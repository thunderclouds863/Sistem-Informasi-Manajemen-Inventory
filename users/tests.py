from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin_test',
            email='admin@tarindo.co.id',
            password='StrongPassword123!',
            is_admin=True,
        )

    def test_login_valid_credentials_redirects_to_dashboard(self):
        resp = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'StrongPassword123!',
            'remember_me': '1',
        })
        self.assertRedirects(resp, reverse('dashboard'))

    def test_login_invalid_credentials_shows_error(self):
        resp = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'wrongpassword',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Invalid username or password')

    def test_logout_redirects_to_login(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, reverse('login'))

    def test_profile_requires_authentication(self):
        resp = self.client.get(reverse('profile'))
        self.assertRedirects(resp, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_password_change_succeeds_and_keeps_session(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('profile'), {
            'old_password': 'StrongPassword123!',
            'new_password1': 'UpdatedPass456!',
            'new_password2': 'UpdatedPass456!',
        })
        self.assertRedirects(resp, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('UpdatedPass456!'))
        # Verify user remains authenticated
        dash = self.client.get(reverse('dashboard'))
        self.assertEqual(dash.status_code, 200)


class PartnerRegistrationAndApprovalTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_app',
            email='admin@tarindo.co.id',
            password='StrongPassword123!',
            is_admin=True,
            is_staff=True,
            is_superuser=True,
        )

    def test_buyer_self_registration_requires_admin_approval(self):
        resp = self.client.post(reverse('register'), {
            'role': 'buyer',
            'name': 'Toko Baru Jaya',
            'address': 'Semarang',
            'email': 'baru@example.com',
            'username': 'buyer_pending',
            'password': 'Password123!',
            'retype_password': 'Password123!',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'pending administrator approval')

        u = User.objects.get(username='buyer_pending')
        self.assertFalse(u.is_active)
        self.assertTrue(u.is_buyer)

        # Cannot log in before approval, receives clear pending message
        login_resp = self.client.post(reverse('login'), {
            'username': 'buyer_pending',
            'password': 'Password123!',
        })
        self.assertEqual(login_resp.status_code, 200)
        self.assertContains(login_resp, 'pending administrator approval')

        # Admin approves account
        self.client.force_login(self.admin)
        approvals_resp = self.client.get(reverse('pending-approvals'))
        self.assertContains(approvals_resp, 'Toko Baru Jaya')

        approve_resp = self.client.post(reverse('approve-account', args=[u.pk]))
        self.assertRedirects(approve_resp, reverse('pending-approvals'))
        u.refresh_from_db()
        self.assertTrue(u.is_active)

        # Approved buyer can now log in
        self.client.logout()
        ok_resp = self.client.post(reverse('login'), {
            'username': 'buyer_pending',
            'password': 'Password123!',
        })
        self.assertRedirects(ok_resp, reverse('dashboard'))

    def test_admin_can_reject_pending_supplier(self):
        self.client.post(reverse('register'), {
            'role': 'supplier',
            'name': 'Pending Vendor',
            'address': 'Pati',
            'email': 'pv@example.com',
            'username': 'sup_pending',
            'password': 'Password123!',
            'retype_password': 'Password123!',
        })
        u = User.objects.get(username='sup_pending')
        self.client.force_login(self.admin)
        resp = self.client.post(reverse('reject-account', args=[u.pk]))
        self.assertRedirects(resp, reverse('pending-approvals'))
        self.assertFalse(User.objects.filter(pk=u.pk).exists())


class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='reset_user',
            email='reset@tarindo.co.id',
            password='OldPassword123!',
            is_admin=True,
        )

    def test_password_reset_full_token_workflow(self):
        from django.core import mail
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        resp = self.client.post(reverse('password_reset'), {'email': 'reset@tarindo.co.id'})
        self.assertRedirects(resp, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        confirm_url = reverse('password_reset_confirm', args=[uid, token])

        get_resp = self.client.get(confirm_url, follow=True)
        self.assertEqual(get_resp.status_code, 200)

        post_resp = self.client.post(get_resp.request['PATH_INFO'], {
            'new_password1': 'NewSecurePass789!',
            'new_password2': 'NewSecurePass789!',
        })
        self.assertRedirects(post_resp, reverse('password_reset_complete'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePass789!'))

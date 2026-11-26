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

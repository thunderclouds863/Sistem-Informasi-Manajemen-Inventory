from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from SI.models import Buyer, Delivery, Drop, Order, Product, Season, Supplier
from users.models import User


class InventoryAuthAndRBACTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin1', password='Password123!', is_admin=True
        )
        self.sup_user1 = User.objects.create_user(
            username='sup1', password='Password123!', email='s1@test.com', is_supplier=True
        )
        self.sup_user2 = User.objects.create_user(
            username='sup2', password='Password123!', email='s2@test.com', is_supplier=True
        )
        self.buy_user1 = User.objects.create_user(
            username='buy1', password='Password123!', email='b1@test.com', is_buyer=True
        )
        self.buy_user2 = User.objects.create_user(
            username='buy2', password='Password123!', email='b2@test.com', is_buyer=True
        )

        self.supplier1 = Supplier.objects.create(user=self.sup_user1, name='Supplier A', address='Tangerang')
        self.supplier2 = Supplier.objects.create(user=self.sup_user2, name='Supplier B', address='Bekasi')
        self.buyer1 = Buyer.objects.create(user=self.buy_user1, name='Buyer A', address='Jakarta')
        self.buyer2 = Buyer.objects.create(user=self.buy_user2, name='Buyer B', address='Bandung')
        self.season = Season.objects.create(name='Q1 2026', description='Quarter 1')
        self.drop = Drop.objects.create(name='Gudang Bahan Baku')
        self.product = Product.objects.create(name='Kran Kuningan 1/2"', sortno=50)

        self.order1 = Order.objects.create(
            supplier=self.supplier1, product=self.product, design='D-101', color='Gold',
            buyer=self.buyer1, season=self.season, drop=self.drop, status='pending',
        )
        self.order2 = Order.objects.create(
            supplier=self.supplier2, product=self.product, design='D-202', color='Silver',
            buyer=self.buyer2, season=self.season, drop=self.drop, status='approved',
        )
        self.delivery1 = Delivery.objects.create(order=self.order1, courier_name='JNE Cargo')
        self.delivery2 = Delivery.objects.create(order=self.order2, courier_name='Lalamove')

    def test_anonymous_cannot_access_any_list_or_dashboard(self):
        protected = [
            'dashboard', 'order-list', 'product-list', 'supplier-list',
            'buyer-list', 'delivery-list', 'season-list', 'drop-list',
        ]
        for name in protected:
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 302, f'{name} should redirect anonymous users')
            self.assertIn(reverse('login'), resp['Location'])

    def test_non_admin_forbidden_from_admin_write_endpoints(self):
        self.client.force_login(self.buy_user1)
        admin_urls = [
            reverse('create-product'),
            reverse('edit-product', args=[self.product.pk]),
            reverse('create-order'),
            reverse('create-supplier'),
            reverse('create-buyer'),
            reverse('create-season'),
            reverse('create-drop'),
            reverse('create-delivery'),
        ]
        for url in admin_urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 403, f'Buyer should get 403 on {url}')

        resp = self.client.post(reverse('update-order-status', args=[self.order1.pk]), {'status': 'complete'})
        self.assertEqual(resp.status_code, 403)

    def test_supplier_and_buyer_only_see_scoped_orders_and_deliveries(self):
        self.client.force_login(self.sup_user1)
        resp = self.client.get(reverse('order-list'))
        self.assertContains(resp, 'D-101')
        self.assertNotContains(resp, 'D-202')

        resp_del = self.client.get(reverse('delivery-list'))
        self.assertContains(resp_del, 'JNE Cargo')
        self.assertNotContains(resp_del, 'Lalamove')

        self.client.force_login(self.buy_user2)
        resp_b = self.client.get(reverse('order-list'))
        self.assertContains(resp_b, 'D-202')
        self.assertNotContains(resp_b, 'D-101')

    def test_delete_endpoints_require_post(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse('delete-product', args=[self.product.pk]))
        self.assertEqual(resp.status_code, 405)


class InventoryCRUDAndWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_crud', password='Password123!', is_admin=True
        )
        self.client.force_login(self.admin)
        sup_u = User.objects.create_user(username='sup_c', password='Password123!', is_supplier=True)
        buy_u = User.objects.create_user(username='buy_c', password='Password123!', is_buyer=True)
        self.supplier = Supplier.objects.create(user=sup_u, name='Logam Prima', address='Surabaya')
        self.buyer = Buyer.objects.create(user=buy_u, name='CV Sanitair', address='Bandung')
        self.season = Season.objects.create(name='Q2 2026', description='Quarter 2')
        self.drop = Drop.objects.create(name='Gudang Barang Jadi')
        self.product = Product.objects.create(name='Stop Kran', sortno=25)

    def test_product_create_edit_delete(self):
        resp = self.client.post(reverse('create-product'), {'name': 'Shower Brass', 'sortno': 120})
        self.assertRedirects(resp, reverse('product-list'))
        p = Product.objects.get(name='Shower Brass')
        self.assertEqual(p.sortno, 120)

        resp = self.client.post(reverse('edit-product', args=[p.pk]), {'name': 'Shower Brass Pro', 'sortno': 95})
        self.assertRedirects(resp, reverse('product-list'))
        p.refresh_from_db()
        self.assertEqual(p.name, 'Shower Brass Pro')
        self.assertEqual(p.sortno, 95)

        resp = self.client.post(reverse('delete-product', args=[p.pk]))
        self.assertRedirects(resp, reverse('product-list'))
        self.assertFalse(Product.objects.filter(pk=p.pk).exists())

    def test_order_lifecycle_create_status_update_edit_delete(self):
        resp = self.client.post(reverse('create-order'), {
            'supplier': self.supplier.pk,
            'product': self.product.pk,
            'design': 'D-500',
            'color': 'Gold',
            'buyer': self.buyer.pk,
            'season': self.season.pk,
            'drop': self.drop.pk,
        })
        self.assertRedirects(resp, reverse('order-list'))
        order = Order.objects.get(design='D-500')
        self.assertEqual(order.status, 'pending')

        # Quick status transition
        resp = self.client.post(reverse('update-order-status', args=[order.pk]), {'status': 'complete'})
        self.assertRedirects(resp, reverse('order-list'))
        order.refresh_from_db()
        self.assertEqual(order.status, 'complete')

        # Invalid status rejected without mutating DB
        self.client.post(reverse('update-order-status', args=[order.pk]), {'status': 'invalid_status'})
        order.refresh_from_db()
        self.assertEqual(order.status, 'complete')

        # Edit order
        resp = self.client.post(reverse('edit-order', args=[order.pk]), {
            'supplier': self.supplier.pk,
            'product': self.product.pk,
            'design': 'D-500-R',
            'color': 'Silver',
            'buyer': self.buyer.pk,
            'season': self.season.pk,
            'drop': self.drop.pk,
            'status': 'processing',
        })
        self.assertRedirects(resp, reverse('order-list'))
        order.refresh_from_db()
        self.assertEqual(order.design, 'D-500-R')
        self.assertEqual(order.status, 'processing')

        # Delete order
        resp = self.client.post(reverse('delete-order', args=[order.pk]))
        self.assertRedirects(resp, reverse('order-list'))
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())

    def test_supplier_password_mismatch_does_not_create_orphaned_user(self):
        resp = self.client.post(reverse('create-supplier'), {
            'name': 'New Foundry',
            'address': 'Pati',
            'email': 'nf@example.com',
            'username': 'new_foundry_u',
            'password': 'Password123',
            'retype_password': 'DifferentPassword',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Passwords do not match.')
        self.assertFalse(User.objects.filter(username='new_foundry_u').exists())
        self.assertFalse(Supplier.objects.filter(name='New Foundry').exists())

    def test_supplier_create_edit_delete_atomic(self):
        resp = self.client.post(reverse('create-supplier'), {
            'name': 'Kuningan Baru',
            'address': 'Juwana',
            'email': 'kb@example.com',
            'username': 'kb_user',
            'password': 'Password123',
            'retype_password': 'Password123',
        })
        self.assertRedirects(resp, reverse('supplier-list'))
        sup = Supplier.objects.get(name='Kuningan Baru')
        self.assertTrue(sup.user.is_supplier)

        resp = self.client.post(reverse('edit-supplier', args=[sup.pk]), {
            'name': 'Kuningan Baru Utama',
            'address': 'Juwana Pati',
            'email': 'updated@example.com',
        })
        self.assertRedirects(resp, reverse('supplier-list'))
        sup.refresh_from_db()
        self.assertEqual(sup.name, 'Kuningan Baru Utama')
        self.assertEqual(sup.user.email, 'updated@example.com')

        user_id = sup.user.pk
        resp = self.client.post(reverse('delete-supplier', args=[sup.pk]))
        self.assertRedirects(resp, reverse('supplier-list'))
        self.assertFalse(Supplier.objects.filter(pk=sup.pk).exists())
        self.assertFalse(User.objects.filter(pk=user_id).exists())

    def test_seed_demo_command_is_idempotent(self):
        out = StringIO()
        call_command('seed_demo', stdout=out)
        count_first = Product.objects.count()
        call_command('seed_demo', stdout=out)
        self.assertEqual(Product.objects.count(), count_first)

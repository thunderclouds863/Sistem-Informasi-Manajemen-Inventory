"""Seed demo users and sample inventory data: python manage.py seed_demo"""
from django.core.management.base import BaseCommand

from SI.models import Buyer, Delivery, Drop, Order, Product, Season, Supplier
from users.models import User


class Command(BaseCommand):
    help = "Create demo accounts and sample data (idempotent)"

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username="demo_admin", defaults={"is_admin": True, "is_staff": True, "is_superuser": True})
        if created:
            admin.set_password("demo123")
            admin.save()
        if Product.objects.exists():
            self.stdout.write("Demo data already present")
            return
        suppliers = []
        for i, (name, addr) in enumerate([("Supplier Kuningan Jaya", "Tangerang"), ("PVC Makmur", "Bekasi"), ("Logam Prima", "Surabaya")], 1):
            u = User.objects.create_user(f"supplier{i}", password="demo123", is_supplier=True)
            suppliers.append(Supplier.objects.create(user=u, name=name, address=addr))
        buyers = []
        for i, (name, addr) in enumerate([("Toko Bangunan Sentosa", "Jakarta"), ("CV Sanitair Abadi", "Bandung")], 1):
            u = User.objects.create_user(f"buyer{i}", password="demo123", is_buyer=True)
            buyers.append(Buyer.objects.create(user=u, name=name, address=addr))
        seasons = [Season.objects.create(name=n, description=d) for n, d in [("Q1 2026", "Kuartal 1"), ("Q2 2026", "Kuartal 2")]]
        drops = [Drop.objects.create(name=n) for n in ["Gudang Bahan Baku", "Gudang Setengah Jadi", "Gudang Barang Jadi"]]
        products = [Product.objects.create(name=n, sortno=k) for k, n in enumerate(
            ["Kran Kuningan 1/2\"", "Kran PVC 3/4\"", "Kran Taman", "Stop Kran", "Shower Kuningan"], 1)]
        statuses = ["pending", "approved", "processing", "complete", "decline", "complete", "approved", "pending"]
        for k, st in enumerate(statuses):
            o = Order.objects.create(supplier=suppliers[k % 3], product=products[k % 5], design=f"D-{100 + k}",
                                     color=["Gold", "Silver", "Putih", "Abu"][k % 4], buyer=buyers[k % 2],
                                     season=seasons[k % 2], drop=drops[k % 3], status=st)
            if st == "complete":
                Delivery.objects.create(order=o, courier_name=["JNE Cargo", "Lalamove"][k % 2])
        self.stdout.write(self.style.SUCCESS("Demo data seeded"))

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

from SI.models import Product, Supplier, Buyer, Order, Delivery, Drop, Season


@login_required(login_url='login')
def dashboard(request):
    total_product = Product.objects.count()
    total_supplier = Supplier.objects.count()
    total_buyer = Buyer.objects.count()
    total_order = Order.objects.count()
    total_delivery = Delivery.objects.count()
    total_drop = Drop.objects.count()
    total_season = Season.objects.count()
    total_stock = Product.objects.aggregate(total=Sum('sortno'))['total'] or 0

    orders = (
        Order.objects.select_related('supplier', 'product', 'buyer', 'season', 'drop')
        .order_by('-id')
    )

    status_counts_raw = dict(
        Order.objects.values('status').annotate(total=Count('id')).values_list('status', 'total')
    )
    status_meta = [
        ('complete', 'Complete', 'emerald'),
        ('approved', 'Approved', 'cobalt'),
        ('processing', 'Processing', 'indigo'),
        ('pending', 'Pending', 'amber'),
        ('bulk', 'Bulk', 'slate'),
        ('decline', 'Decline', 'rose'),
    ]
    status_summary = []
    for key, label, tone in status_meta:
        count = status_counts_raw.get(key, 0)
        pct = round((count / total_order) * 100) if total_order else 0
        status_summary.append({
            'key': key,
            'label': label,
            'tone': tone,
            'count': count,
            'pct': pct,
        })

    products = list(Product.objects.all().order_by('-sortno')[:6])
    max_stock = max((p.sortno for p in products), default=1) or 1
    for p in products:
        p.stock_pct = min(100, round((p.sortno / max_stock) * 100))

    drops = Drop.objects.annotate(order_count=Count('order')).order_by('name')
    recent_deliveries = (
        Delivery.objects.select_related('order', 'order__product', 'order__buyer')
        .order_by('-id')[:4]
    )

    context = {
        'product': total_product,
        'supplier': total_supplier,
        'buyer': total_buyer,
        'order': total_order,
        'orders': orders,
        'delivery_count': total_delivery,
        'drop_count': total_drop,
        'season_count': total_season,
        'total_stock': total_stock,
        'pending_count': status_counts_raw.get('pending', 0),
        'complete_count': status_counts_raw.get('complete', 0),
        'status_summary': status_summary,
        'products': products,
        'drops': drops,
        'recent_deliveries': recent_deliveries,
    }
    return render(request, 'dashboard.html', context)

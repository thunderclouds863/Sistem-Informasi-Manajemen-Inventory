from django.db.models import Q

from SI.permissions import is_admin_user
from users.models import User


def pending_approvals_count(request):
    if is_admin_user(getattr(request, 'user', None)):
        count = User.objects.filter(is_active=False).filter(
            Q(is_supplier=True) | Q(is_buyer=True)
        ).count()
        return {'pending_approvals_count': count}
    return {'pending_approvals_count': 0}

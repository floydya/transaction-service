from django.db.models import Sum, Q
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.models import Account
from app.serializers import AccountSerializer

__all__ = "AccountViewSet",


class AccountViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all().annotate(
        total=Sum(
            'wallets__transactions__amount',
            filter=Q(wallets__transactions__canceled=False)
        )
    ).prefetch_related('wallets')
    lookup_field = 'code'

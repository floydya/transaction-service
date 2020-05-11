from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from app.models import Account
from app.serializers import WalletSerializer

__all__ = "WalletViewSet",


class WalletViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = WalletSerializer
    lookup_field = 'code'

    def get_queryset(self):
        account_code = self.kwargs.get('account_code')
        account = get_object_or_404(Account, code=account_code)
        return account.wallets.all()

    def get_serializer_context(self):
        context = super(WalletViewSet, self).get_serializer_context()
        context['account_code'] = self.kwargs.get('account_code')
        return context

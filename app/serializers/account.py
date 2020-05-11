from rest_framework import serializers

from app.models import Account

__all__ = "AccountSerializer",

from app.serializers.wallet import WalletSerializer


class AccountSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    code = serializers.ReadOnlyField()
    wallets = WalletSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = 'id', 'code', 'name', 'hook_url', 'wallets', 'total',

from rest_framework import serializers

from app.models import Wallet

__all__ = "WalletSerializer",


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = 'id', 'name'
        read_only_fields = fields

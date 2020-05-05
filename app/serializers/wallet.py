from rest_framework import serializers

from app.models import Wallet, Account

__all__ = "WalletSerializer",


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = 'id', 'code', 'name', 'account', 'type'
        read_only_fields = 'id', 'code', 'account'

    def validate(self, attrs):
        try:
            attrs['account'] = Account.objects.get(code=self.context.get('account_code'))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No account with {}".format(self.context.get('account_code')))
        return attrs

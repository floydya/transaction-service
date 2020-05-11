from rest_framework import serializers

from app.models import Wallet, Account

__all__ = "WalletSerializer",


class WalletSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    @staticmethod
    def get_total(obj: Wallet):
        return obj.transactions.affirmed().total()

    class Meta:
        model = Wallet
        fields = 'id', 'code', 'name', 'account', 'type', 'total'
        read_only_fields = 'id', 'code', 'account', 'total'

    def validate(self, attrs):
        try:
            attrs['account'] = Account.objects.get(code=self.context.get('account_code'))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No account with {}".format(self.context.get('account_code')))
        return attrs

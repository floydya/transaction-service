from rest_framework import serializers

from app.models import Account

__all__ = "AccountSerializer",


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = 'id', 'code', 'name', 'hook_url'
        read_only_fields = 'id', 'code',

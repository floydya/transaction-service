from rest_framework import serializers

from app.models import Transaction, Wallet

__all__ = "TransactionSerializer", "TransactionCancelSerializer"


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    code = serializers.ReadOnlyField()
    wallet = serializers.SlugRelatedField(
        queryset=Wallet.objects.all(),
        slug_field="code"
    )
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    timestamp = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "code",
            "wallet",
            "content_type_id",
            "entity_id",
            "amount",
            "description",
            "timestamp",
        )


class TransactionCancelSerializer(serializers.Serializer):
    canceled_by = serializers.IntegerField(allow_null=True, required=True)
    canceled_reason = serializers.CharField(allow_null=True, required=True, max_length=512)

    def update(self, instance: Transaction, validated_data):
        return instance.cancel(**validated_data)

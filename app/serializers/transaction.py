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
    type = serializers.ReadOnlyField()
    description = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "code",
            "type",
            "wallet",
            "content_type_id",
            "entity_id",
            "amount",
            "description",
            "timestamp",
        )

    def create(self, validated_data):
        return Transaction.create(**validated_data)


class TransactionCancelSerializer(serializers.Serializer):
    initiator = serializers.CharField(allow_null=True, required=True)

    def update(self, instance: Transaction, validated_data):
        return instance.cancel(validated_data.get('initiator', None))

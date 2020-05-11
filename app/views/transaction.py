from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.filters import TransactionFilter
from app.models import Transaction
from app.pagination import TransactionPagination
from app.serializers import TransactionSerializer, TransactionCancelSerializer

__all__ = 'TransactionViewSet',


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter
    lookup_url_kwarg = "code"
    lookup_field = "code"
    pagination_class = TransactionPagination

    @action(detail=True, methods=["post"])
    def cancel(self, request, code=None):
        transaction = self.get_object()
        serializer = TransactionCancelSerializer(instance=transaction, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data)

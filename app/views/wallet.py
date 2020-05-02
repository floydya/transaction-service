from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

from app.filters import TransactionFilter
from app.models import Wallet
from app.serializers import WalletSerializer

__all__ = "wallet_create", "wallet_info"


@api_view(["POST"])
def wallet_create(request: Request):
    serializer = WalletSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    try:
        headers = {'Location': str(serializer.data[api_settings.URL_FIELD_NAME])}
    except (TypeError, KeyError):
        headers = {}
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(["GET"])
def wallet_info(request: Request, wallet_id):
    wallet = get_object_or_404(Wallet, pk=wallet_id)
    f = TransactionFilter(request.query_params, wallet.transactions.affirmed())
    total_amount = f.qs.total()
    return Response(
        {
            "wallet": wallet_id,
            "total": total_amount
        }
    )

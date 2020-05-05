from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.filters import TransactionFilter
from app.models import Account
from app.serializers import AccountSerializer, WalletSerializer

__all__ = "account_create", "account_info"


class CreateAccountView(CreateAPIView):
    serializer_class = AccountSerializer


account_create = CreateAccountView.as_view()


@api_view(["GET"])
def account_info(request: Request, account_code):
    account = get_object_or_404(Account, code=account_code)
    wallets = [{
        "wallet": WalletSerializer(wallet).data,
        "total": TransactionFilter(request.query_params, wallet.transactions.affirmed()).qs.total() or 0
    } for wallet in account.wallets.all()]
    return Response(
        {
            "account": AccountSerializer(account).data,
            "wallets": wallets,
            "total": sum((a["total"] for a in wallets))
        }
    )

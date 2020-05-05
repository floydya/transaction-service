from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.filters import TransactionFilter
from app.models import Wallet
from app.serializers import WalletSerializer

__all__ = "wallet_create", "wallet_info"


class WalletCreateView(CreateAPIView):
    serializer_class = WalletSerializer

    def get_serializer_context(self):
        context = super(WalletCreateView, self).get_serializer_context()
        context['account_code'] = self.kwargs.get('account_code')
        return context


wallet_create = WalletCreateView.as_view()


@api_view(["GET"])
def wallet_info(request: Request, account_code, wallet_code):
    wallet = get_object_or_404(Wallet, account__code=account_code, code=wallet_code)
    f = TransactionFilter(request.query_params, wallet.transactions.affirmed())
    total_amount = f.qs.total() or 0
    return Response(
        {
            "wallet": WalletSerializer(wallet).data,
            "total": total_amount
        }
    )

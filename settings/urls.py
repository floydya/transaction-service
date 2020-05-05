from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view

from app.views import (
    TransactionViewSet,
    wallet_info, wallet_create,
    account_create, account_info,
)

schema_view = get_swagger_view(title='Transactions API')

router = SimpleRouter()
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
                  path("accounts/", account_create),
                  path("accounts/<uuid:account_code>/", account_info),
                  path("accounts/<uuid:account_code>/wallets/", wallet_create),
                  path("accounts/<uuid:account_code>/wallets/<uuid:wallet_code>/", wallet_info),
                  path("", schema_view),
              ] + router.urls

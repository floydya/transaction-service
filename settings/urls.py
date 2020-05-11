from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from app.views import (
    TransactionViewSet, AccountViewSet, WalletViewSet
)

schema_view = get_swagger_view(title='Transactions API')

router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")
router.register("accounts", AccountViewSet, basename="accounts")
router.register("accounts/(?P<account_code>[^/.]+)/wallets", WalletViewSet, basename="wallets")

urlpatterns = [
    path("docs/", schema_view),
]

urlpatterns += router.urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

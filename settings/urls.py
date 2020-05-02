from django.urls import path

from rest_framework.routers import SimpleRouter

from app.views import TransactionViewSet, wallet_info, wallet_create

router = SimpleRouter()
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("wallet/", wallet_create),
    path("wallet/<uuid:wallet_id>/", wallet_info),
] + router.urls

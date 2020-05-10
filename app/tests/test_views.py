import json

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import RequestsClient

from app.filters import TransactionFilter
from app.models import Account, Wallet, Transaction
from app.serializers import AccountSerializer, WalletSerializer


class AccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = RequestsClient()
        cls.account = Account.objects.create(name="Test")
        cls.wallet = Wallet.objects.create(account=cls.account, name="Test wallet", type="real")

    def test_account_info(self):
        response = self.client.get(self.account.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), {
            "account": AccountSerializer(self.account).data,
            "wallets": [
                {
                    "wallet": WalletSerializer(self.wallet).data,
                    "total": 0
                }
            ],
            "total": 0
        })


class WalletTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = RequestsClient()
        cls.account = Account.objects.create(name="Test")
        cls.wallet = Wallet.objects.create(account=cls.account, name="Test wallet", type="virtual")
        Transaction.objects.create(wallet=cls.wallet, amount=500)
        Transaction.objects.create(wallet=cls.wallet, amount=-100)

    def test_wallet_info(self):
        response = self.client.get(self.wallet.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), {
            "wallet": WalletSerializer(self.wallet).data,
            "total": 400
        })

    def test_wallet_create(self):
        response = self.client.post(
            reverse('wallet_create', kwargs={"account_code": self.account.code}),
            {"name": "Test1", "type": "real"}
        )
        self.assertEquals(response.status_code, 201)
        wallet_id = json.loads(str(response.content, encoding="utf8")).get('id')
        w = Wallet.objects.get(pk=wallet_id)
        self.assertEquals(w.account_id, self.account.id)

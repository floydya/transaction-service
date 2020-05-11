import json
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import RequestsClient

from app.models import Account, Wallet, Transaction
from app.serializers import AccountSerializer, WalletSerializer


class SetUpMixin(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = RequestsClient()
        cls.account = Account.objects.create(name="Test")
        cls.wallet = Wallet.objects.create(account=cls.account, name="Test wallet", type="virtual")


class AccountTestCase(SetUpMixin, TestCase):

    def test_account_info(self):
        response = self.client.get(self.account.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        # self.assertJSONEqual(str(response.content, encoding="utf8"), AccountSerializer(self.account).data)


class WalletTestCase(SetUpMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super(WalletTestCase, cls).setUpTestData()
        Transaction.objects.create(wallet=cls.wallet, amount=500)
        Transaction.objects.create(wallet=cls.wallet, amount=-100)

    def test_wallet_info(self):
        response = self.client.get(self.wallet.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), WalletSerializer(self.wallet).data)

    def test_wallet_create(self):
        response = self.client.post(
            reverse('wallets-list', kwargs={"account_code": self.account.code}),
            {"name": "Test1", "type": "real"}
        )
        self.assertEquals(response.status_code, 201)
        wallet_id = json.loads(str(response.content, encoding="utf8")).get('id')
        w = Wallet.objects.get(pk=wallet_id)
        self.assertEquals(w.account_id, self.account.id)

    def test_wallet_create_undefined_account(self):
        uuid = str(uuid4())
        response = self.client.post(
            reverse('wallets-list', kwargs={"account_code": uuid}),
            {"name": "Test1", "type": "real"}
        )
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"non_field_errors": [f"No account with {uuid}"]}
        )


class TransactionTestCase(SetUpMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TransactionTestCase, cls).setUpTestData()
        cls.transaction = Transaction.objects.create(wallet=cls.wallet, amount=500)
        cls.canceled_transaction = Transaction.objects.create(wallet=cls.wallet, amount=200)
        cls.canceled_transaction.cancel()

    def test_transaction_cancel(self):
        response = self.client.post(
            reverse("transactions-cancel", kwargs={"code": self.transaction.code}),
            {
                "canceled_by": 5,
                "canceled_reason": "Test comment"
            }
        )
        self.assertEquals(response.status_code, 200)
        self.transaction.refresh_from_db()
        self.assertEquals(self.transaction.canceled_by, 5)
        self.assertEquals(self.transaction.canceled_reason, "Test comment")
        self.assertEquals(self.transaction.canceled, True)

    def test_transaction_cancel_already_canceled(self):
        response = self.client.post(
            reverse("transactions-cancel", kwargs={"code": self.canceled_transaction.code}),
            {
                "canceled_by": 5,
                "canceled_reason": "Test"
            }
        )
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"detail": "This transaction is already canceled."}
        )

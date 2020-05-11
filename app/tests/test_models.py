from django.test import TestCase

from app.models import Account, Wallet, Transaction


class AccountTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(name="Account")

    def test_name_max_length(self):
        max_length = self.account._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)

    def test_account_str(self):
        self.assertEquals(
            str(self.account),
            str(self.account.code)
        )

    def test_get_absolute_url(self):
        self.assertEquals(
            self.account.get_absolute_url(),
            "/accounts/{}/".format(self.account.code)
        )


class WalletTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(name="Account")
        cls.wallet = cls.account.wallets.create(name="Real wallet", type=Wallet.TypeChoices.REAL)

    def test_name_max_length(self):
        max_length = self.wallet._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)

    def test_type_max_length(self):
        max_length = self.wallet._meta.get_field('type').max_length
        self.assertEquals(max_length, 8)

    def test_str_method(self):
        self.assertEquals(
            str(self.wallet),
            str(self.wallet.code)
        )

    def test_get_absolute_url(self):
        self.assertEquals(
            self.wallet.get_absolute_url(),
            "/accounts/{}/wallets/{}/".format(self.account.code, self.wallet.code)
        )


class TransactionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(name="Account")
        cls.wallet1 = cls.account.wallets.create(name="Real wallet", type=Wallet.TypeChoices.REAL)
        cls.wallet2 = cls.account.wallets.create(name="Virtual wallet", type=Wallet.TypeChoices.VIRTUAL)
        cls.transaction = Transaction.objects.create(wallet=cls.wallet1, amount=500)

    def test_str_method(self):
        self.assertEquals(
            str(self.transaction.code),
            str(self.transaction)
        )

    def test_get_absolute_url(self):
        self.assertEquals(self.transaction.get_absolute_url(), f"/transactions/{self.transaction.code}/")

    def test_amount_max_digits(self):
        max_digits = self.transaction._meta.get_field('amount').max_digits
        self.assertEquals(max_digits, 14)

    def test_amount_decimal_places(self):
        decimal_places = self.transaction._meta.get_field('amount').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(wallet=self.wallet1, amount=400)
        self.assertEquals(transaction.description, "")
        self.assertIsNotNone(transaction.timestamp)

    def test_transaction_negative_balance(self):
        try:
            Transaction.objects.create(wallet=self.wallet1, amount=-1000)
            self.fail()
        except AssertionError as e:
            self.assertEquals(str(e), "Balance after transaction will be negative.")

    def test_non_empty_description_on_create(self):
        transaction = Transaction.objects.create(wallet=self.wallet1, amount=400, description="Test description")
        self.assertEquals(transaction.description, "Test description")

    def test_non_empty_timestamp_on_create(self):
        transaction = Transaction.objects.create(wallet=self.wallet1, amount=200, timestamp="2020-01-02T00:00:00")
        self.assertEquals(transaction.timestamp.isoformat(), "2020-01-01T22:00:00+00:00")
        transaction2 = Transaction.objects.create(wallet=self.wallet1, amount=200, timestamp="2020-06-02T00:00:00")
        self.assertEquals(transaction2.timestamp.isoformat(), "2020-06-01T21:00:00+00:00")

    def test_cancel_without_data(self):
        t = Transaction.objects.create(wallet=self.wallet1, amount=500)
        t.cancel()
        t.refresh_from_db()
        self.assertEquals(t.canceled, True)
        self.assertEquals(t.canceled_by, None)
        self.assertEquals(t.canceled_reason, None)
        self.assertIsNotNone(t.canceled_at)

    def test_cancel_with_data(self):
        t = Transaction.objects.create(wallet=self.wallet1, amount=100)
        t.cancel(canceled_by=5, canceled_reason="Test cancel")
        t.refresh_from_db()
        self.assertEquals(t.canceled, True)
        self.assertEquals(t.canceled_by, 5)
        self.assertEquals(t.canceled_reason, "Test cancel")
        self.assertIsNotNone(t.canceled_at)

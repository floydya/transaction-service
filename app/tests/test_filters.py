from django.test import TestCase

from app.filters import TransactionFilter
from app.models import Account, Transaction


class FilterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create(name="Account")
        cls.wallet = cls.account.wallets.create(name="Wallet", type="real")
        for i in range(1, 21):
            Transaction.objects.create(
                wallet=cls.wallet,
                amount=400,
                timestamp="2020-06-{:02}T00:00:00".format(int(i / 2 + 1))
            )

    def test_before_timestamp(self):
        qs = Transaction.objects.affirmed()
        f = TransactionFilter({"before": "2020-06-07T23:59:59"}, qs)
        self.assertEquals(f.qs.count(), 13)

    def test_after_timestamp(self):
        qs = Transaction.objects.affirmed()
        f = TransactionFilter({"after": "2020-06-07T23:59:59"}, qs)
        self.assertEquals(f.qs.count(), 7)

    def test_date_filter_with_total(self):
        qs = Transaction.objects.affirmed()
        f = TransactionFilter({"date": "2020-06-07"}, qs)
        self.assertEquals(f.qs.count(), 2)
        total = f.qs.total()
        self.assertEquals(total, 800)

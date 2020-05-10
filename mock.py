from datetime import datetime
import random
import time

from django.utils.timezone import get_current_timezone

from app.models import Account, Wallet, Transaction


def random_date(start, end):
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    return dt


for i in range(40):
    account = Account.objects.create(name="Account {}".format(i))
    ws = (
        Wallet(
            name="Wallet {}".format(wi),
            account=account,
            type=(Wallet.TypeChoices.REAL, Wallet.TypeChoices.VIRTUAL)[wi == 0]
        )
        for wi in range(2)
    )
    Wallet.objects.bulk_create(ws)

wallets = Wallet.objects.all()
timezone = get_current_timezone()
transactions = []
for i in range(100000):
    Transaction.create(
        wallet=random.choice(wallets),
        content_type_id=random.randint(1, 1000),
        entity_id=random.randint(1, 10000),
        amount=random.randint(200, 10000),
        description="Iteration #{}".format(i),
        timestamp=timezone.localize(random_date("01-01-2019 00:00:00", "01-01-2021 00:00:00"), is_dst=True)
    )

from uuid import uuid4

from django.conf import settings
from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from app.utils import time_string_as_utc as tsau, date_scopes

__all__ = "Transaction",


class TransactionManager(models.Manager):

    def affirmed(self):
        qs = self.get_queryset()
        affirmed_qs = qs.filter(type__in=(
            self.model.TransactionTypes.DEPOSIT,
            self.model.TransactionTypes.WITHDRAW
        ))
        return affirmed_qs


class TransactionQuerySet(models.QuerySet):

    def date(self, date: str, tz=settings.TIME_ZONE):
        _from, _to = date_scopes(date, tz)
        return self.in_range(_from, _to, tz=tz)

    def after(self, timestamp, tz=settings.TIME_ZONE):
        timestamp = tsau(timestamp, tz)
        return self.filter(timestamp__gte=timestamp)

    def before(self, timestamp, tz=settings.TIME_ZONE):
        timestamp = tsau(timestamp, tz)
        return self.filter(timestamp__lte=timestamp)

    def in_range(self, _from, _to, tz=settings.TIME_ZONE):
        return self.after(_from, tz).before(_to, tz)

    def wallet(self, wallet_code):
        return self.filter(wallet__code=wallet_code)

    def account(self, account_code, _type=None):
        qs = self.filter(wallet__account__code=account_code)
        if _type is not None:
            qs = qs.filter(wallet__type=_type)
        return qs

    def total(self):
        aggregation = self.aggregate(total=models.Sum('amount'))
        return aggregation.get('total', 0)


class Transaction(models.Model):
    class Meta:
        verbose_name_plural = _("Transactions")
        db_table = "transactions"

    class TransactionTypes(models.TextChoices):
        DEPOSIT = 'deposit', _("Deposit")
        WITHDRAW = 'withdraw', _("Withdraw")
        CANCELED = 'canceled', _("Canceled")

    code = models.UUIDField(default=uuid4, unique=True, db_index=True)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(choices=TransactionTypes.choices, max_length=8)
    content_type_id = models.PositiveIntegerField()
    entity_id = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField()

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    def __str__(self):
        return str(self.code)

    @classmethod
    @transaction.atomic
    def create(cls, wallet, content_type_id, entity_id, amount, description=None, timestamp=None):
        if amount < 0:
            wallet_total = wallet.transactions.affirmed().total()
            assert wallet_total + amount >= 0, "Balance after transaction will be negative."

        transaction_type = cls.TransactionTypes.DEPOSIT if amount > 0 else cls.TransactionTypes.WITHDRAW

        if description is None:
            description = ""
        if timestamp is None:
            timestamp = now()

        return cls.objects.create(
            wallet=wallet,
            type=transaction_type,
            content_type_id=content_type_id,
            entity_id=entity_id,
            amount=amount,
            description=description,
            timestamp=timestamp
        )

    @transaction.atomic
    def update(self, **kwargs):
        print([f.name for f in self._meta.fields])
        assert all(kwarg in (f.name for f in self._meta.fields) for kwarg in kwargs), "Undefined kwarg"

        if "amount" in kwargs.keys():
            self.amount = kwargs.get("amount")
            self.type = self.TransactionTypes.DEPOSIT if self.amount > 0 else self.TransactionTypes.WITHDRAW

        return self

    def cancel(self, initiator=None):
        assert self.type != self.TransactionTypes.CANCELED, "This transaction is already canceled."

        self.type = self.TransactionTypes.CANCELED
        if initiator is None:
            initiator = "System"
        self.description = f"{self.description} # Canceled by {initiator} at {now()}"
        self.save(update_fields=("type", "description"))
        return self

from uuid import uuid4

from django.conf import settings
from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from app.choices.transaction import TypeChoices
from app.utils import time_string_as_utc as tsau, date_scopes

__all__ = "Transaction",


class TransactionManager(models.Manager):

    def non_zero(self):
        qs = self.get_queryset()
        non_zero_qs = qs.filter(type__in=(
            TypeChoices.DEPOSIT,
            TypeChoices.WITHDRAW,
        ))
        return non_zero_qs

    def affirmed(self):
        qs = self.get_queryset()
        affirmed_qs = qs.filter(type__in=(
            TypeChoices.DEPOSIT,
            TypeChoices.WITHDRAW,
            TypeChoices.ZERO
        ))
        return affirmed_qs


class TransactionQuerySet(models.QuerySet):

    @transaction.atomic
    def create(self, wallet, amount, content_type_id=None, entity_id=None, description=None, timestamp=None, type=None):
        if amount < 0:
            wallet_total = wallet.transactions.affirmed().total()
            assert wallet_total + amount >= 0, "Balance after transaction will be negative."

        transaction_type = TypeChoices.correlate_amount(amount)

        if description is None:
            description = ""

        if timestamp is None:
            timestamp = now()
        elif isinstance(timestamp, str):
            timestamp = tsau(timestamp, settings.TIME_ZONE)

        obj = self.model(
            wallet=wallet,
            type=transaction_type,
            content_type_id=content_type_id,
            entity_id=entity_id,
            amount=amount,
            description=description,
            timestamp=timestamp
        )
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def date(self, date: str, tz=settings.TIME_ZONE):
        _from, _to = date_scopes(date, tz)
        return self.in_range(_from, _to, tz=tz)

    def after(self, timestamp, tz=settings.TIME_ZONE):
        timestamp = tsau(timestamp, tz)
        return self.filter(timestamp__gte=timestamp)

    def before(self, timestamp, tz=settings.TIME_ZONE):
        timestamp = tsau(timestamp, tz)
        return self.filter(timestamp__lte=timestamp)

    def total(self):
        aggregation = self.aggregate(total=models.Sum('amount'))
        return aggregation.get('total', 0)


class Transaction(models.Model):
    TransactionTypes = TypeChoices

    class Meta:
        verbose_name_plural = _("Transactions")
        db_table = "transactions"

    code = models.UUIDField(default=uuid4, unique=True, db_index=True)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(choices=TransactionTypes.choices, max_length=8)
    content_type_id = models.PositiveIntegerField(null=True)
    entity_id = models.PositiveIntegerField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField()

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    def __str__(self):
        return str(self.code)

    @transaction.atomic
    def update(self, **kwargs):
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

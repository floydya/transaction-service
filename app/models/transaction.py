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
        return qs.filter(canceled=False)


class TransactionQuerySet(models.QuerySet):

    @transaction.atomic
    def create(self, wallet, amount, content_type_id=None, entity_id=None, description=None, timestamp=None):
        if amount < 0:
            wallet_total = wallet.transactions.affirmed().total()
            assert wallet_total + amount >= 0, "Balance after transaction will be negative."

        if description is None:
            description = ""

        if timestamp is None:
            timestamp = now()
        elif isinstance(timestamp, str):
            timestamp = tsau(timestamp, settings.TIME_ZONE)

        obj = self.model(
            wallet=wallet,
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
        return self.after(_from, tz=tz).before(_to, tz=tz)

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
    class Meta:
        verbose_name_plural = _("Transactions")
        db_table = "transactions"

    code = models.UUIDField(default=uuid4, unique=True, db_index=True)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name="transactions")
    content_type_id = models.PositiveIntegerField(null=True)
    entity_id = models.PositiveIntegerField(null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField(default="")
    timestamp = models.DateTimeField(default=now)

    canceled = models.BooleanField(default=False)
    canceled_by = models.PositiveIntegerField(null=True)
    canceled_at = models.DateTimeField(null=True)
    canceled_reason = models.TextField(null=True)

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    def __str__(self):
        return str(self.code)

    def cancel(self, canceled_by=None, comment=None):
        assert not self.canceled, "This transaction is already canceled."
        self.canceled = True
        self.canceled_by = canceled_by or None
        self.canceled_reason = comment or None
        self.canceled_at = now()
        self.save(update_fields=("canceled", "canceled_by", "canceled_reason", "canceled_at"))
        return self

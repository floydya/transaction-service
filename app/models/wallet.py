from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

__all__ = "Wallet",


class Wallet(models.Model):
    class Meta:
        verbose_name_plural = _("Wallets")
        db_table = "wallets"

    class TypeChoices(models.TextChoices):
        REAL = "real", _("Real")
        VIRTUAL = "virtual", _("Virtual")

    code = models.UUIDField(default=uuid4, unique=True, db_index=True)
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=64)
    type = models.CharField(choices=TypeChoices.choices, max_length=8, db_index=True)

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse('wallet_info', kwargs={"account_code": self.account.code, "wallet_code": self.code})

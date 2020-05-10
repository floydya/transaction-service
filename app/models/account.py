from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

__all__ = "Account",


class Account(models.Model):
    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        db_table = "accounts"

    code = models.UUIDField(default=uuid4, unique=True, db_index=True)
    name = models.CharField(max_length=64)
    hook_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse("account_info", kwargs={"account_code": self.code})

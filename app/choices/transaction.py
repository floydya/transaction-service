from django.db.models.enums import TextChoices

from django.utils.translation import gettext_lazy as _

__all__ = "TypeChoices",


class TypeChoices(TextChoices):
    DEPOSIT = 'deposit', _("Deposit")
    WITHDRAW = 'withdraw', _("Withdraw")
    ZERO = 'zero', _("Zero")
    CANCELED = 'canceled', _("Canceled")

    @classmethod
    def correlate_amount(cls, amount):
        # 😿 Легче проще чем сложнее, если бы не это, могло быть так:
        # return ((cls.WITHDRAW, cls.ZERO)[amount == 0], cls.DEPOSIT)[amount > 0]
        if amount > 0:
            return cls.DEPOSIT
        elif amount < 0:
            return cls.WITHDRAW
        return cls.ZERO

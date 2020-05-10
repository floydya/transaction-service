from datetime import datetime

import django_filters

from app.models import Transaction

__all__ = "TransactionFilter",


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ('before', 'after', 'date', 'wallet', 'account', 'amount')

    amount_from = django_filters.NumberFilter(field_name="amount", lookup_expr="gte", label="Greater than equal")
    amount_to = django_filters.NumberFilter(field_name="amount", lookup_expr="lte", label="Less than equal")
    before = django_filters.IsoDateTimeFilter(method='get_before', label="Before date")
    after = django_filters.IsoDateTimeFilter(method='get_after', label="After date")
    date = django_filters.DateFilter(method='get_by_date', label="Date")
    wallet = django_filters.UUIDFilter(field_name="wallet_id")
    account = django_filters.UUIDFilter(field_name="wallet__account_id")

    def get_before(self, queryset, name, value: datetime):
        return queryset.before(value)

    def get_after(self, queryset, name, value: datetime):
        return queryset.after(value)

    def get_by_date(self, queryset, name, value):
        return queryset.date(str(value))

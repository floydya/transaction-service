from datetime import datetime

import django_filters

from app.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ('before', 'after', 'date', 'type', 'wallet', 'account')

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

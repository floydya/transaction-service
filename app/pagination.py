from rest_framework import pagination

__all__ = "TransactionPagination",


class TransactionPagination(pagination.LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AssertionError):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return response

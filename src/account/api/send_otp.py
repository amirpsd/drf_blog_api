from django.core.cache import cache
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from extensions.utils import otp_generator, get_client_ip


# send otp code


def send_otp(request, phone):
    otp = otp_generator()
    ip = get_client_ip(request)
    cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

    # TODO Here the otp code must later be sent to the user's phone number by SMS system.
    # But in debug mode we return the otp code.

    context = {
        "otp": f"{otp}",
    }
    return Response(
        context,
        status=status.HTTP_200_OK,
    )
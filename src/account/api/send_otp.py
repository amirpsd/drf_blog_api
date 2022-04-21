from django.core.cache import cache
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from ..models import PhoneOtp 
from extensions.code_generator import otp_generator


# send otp code 

def send_otp(*, phone: str):
    user_otp, _ = PhoneOtp.objects.get_or_create(
        phone=phone,
    )
    otp = otp_generator()
    user_otp.otp = otp
    user_otp.save(update_fields=["otp"])
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

    # Here the otp code must later be sent to the user's phone number by SMS system.
    print(f"your phone: {phone}")
    print(f"your otp code :: {otp} ")
    # But in debug mode we print the otp code.

    context = {
        "code sent.": "The code has been sent to the desired phone number.",
    }
    return Response(
        context, 
        status=status.HTTP_200_OK,
    )
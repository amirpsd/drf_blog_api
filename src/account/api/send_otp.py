from django.core.cache import cache
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from extensions.code_generator import otp_generator


# send otp code 

def send_otp(*, user_otp: object, phone: str):
    otp = otp_generator()
    user_otp.otp = otp
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

    # Here the otp code must later be sent to the user's phone number by SMS system.
    print(f"your phone: {phone}")
    print(f"your otp code :: {otp} ")
    # But in debug mode we print the otp code.

    user_otp.count += 1
    user_otp.save(update_fields=["otp", "count"])

    context = {
        "code sent.": "The code has been sent to the desired phone number.",
    }
    return Response(
        context, 
        status=status.HTTP_200_OK,
    )
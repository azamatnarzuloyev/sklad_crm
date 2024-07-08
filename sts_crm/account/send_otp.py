import requests
from django.core.cache import cache
from extensions.code_generator import otp_generator, get_client_ip
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from config.config.application import EXPIRY_TIME_OTP , SMS_TOKEN
from magazin.models import AllShop
# send otp code 
def send_otp(request, phone):
    otp = otp_generator()
 
    ip = get_client_ip(request)
    # user_otp.otp = otp
    cache.set(f"{ip}-for-authentication", phone, EXPIRY_TIME_OTP)
    cache.set(phone, otp, EXPIRY_TIME_OTP)
    print(otp)

    url = f'http://notify.eskiz.uz/api/message/sms/send?mobile_phone={phone}&from=4546&message=sts-hik.uz web site uchun kirish code: {otp} ) '
    headers = {'Authorization': f'Bearer {SMS_TOKEN}'}


    response = requests.post(url, headers=headers)
    data_set = {
        "otp": otp,
        "errors": False,
        "message": "",
        "sms_provayder": response.json()

    }
    return Response(
        data_set,
        status=status.HTTP_200_OK,
    )

def send_otp_dokon(request, phone):
    otp = otp_generator()
    ip = get_client_ip(request)
    user = request.user
    all_shop = AllShop.objects.get(userId__id=user.id)
    shop_name = all_shop.dokon_name
    # user_otp.otp = otp
    cache.set(f"{ip}-for-authentication", phone, EXPIRY_TIME_OTP)
    cache.set(phone, otp, EXPIRY_TIME_OTP)
    print(otp)

    url = f'http://notify.eskiz.uz/api/message/sms/send?mobile_phone={phone}&from=4546&message= {shop_name} Yangi mijoz ochish uchun parol: {otp} (sizning ip manzilingiz  {ip})'
    headers = {'Authorization': f'Bearer {SMS_TOKEN}'}


    response = requests.post(url, headers=headers)
    return Response(
        # response.json(),
        data={"sms": otp},
        status=status.HTTP_200_OK,
    )
import jwt
import time, hmac, base64, hashlib, json, requests
from functools import wraps

from django.http import JsonResponse

from my_settings import SECRET_KEY, ENCRYPTION_ALGORITHM, ACCESS_KEY_ID#, SMS_SEND_PHONE_NUMBER, SMS_URL, SERVICE_SECRET_KEY, URI
from user.models import User


REGEX_PHONE_NUMBER = '^01([0|1|6|7|8|9]?)?([0-9]{8,9})$'
REGEX_PASSWORD = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'  # 영문+숫자+특수문자 10자 이상
REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def login_required(func):
    @wraps(func)
    def decorated_function(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                decoded_access_token = jwt.decode(access_token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)
                email                = decoded_access_token['id']
                user                 = User.objects.get(email=email)
                request.user         = user
            except jwt.InvalidTokenError:
                return JsonResponse({'MESSAGE': 'INVALID ACCESS TOKEN'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'MESSAGE': 'USER NOT EXIST'}, status=401)
        else:
            return JsonResponse({'MESSAGE': 'ACCESS TOKEN NOT EXIST'}, status=401)

        return func(self, request, *args, **kwargs)
    return decorated_function


def send_sms(phone_number, sms_number):
    time_stamp = str(int(time.time() * 1000))

    plain_text = bytes("POST " + URI + "\n" + time_stamp + "\n" + ACCESS_KEY_ID, 'UTF-8')
    secret_key = bytes(SERVICE_SECRET_KEY, 'UTF-8')
    hmac_signature = hmac.new(secret_key, plain_text, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hmac_signature).decode('UTF-8')

    headers = {
        "Content-Type"            : "application/json; charset=UTF-8",
        'x-ncp-apigw-timestamp'   : f'{time_stamp}',
        'x-ncp-iam-access-key'    : f'{ACCESS_KEY_ID}',
        "x-ncp-apigw-signature-v2": f'{signature}',
    }
    data = {
        'type'       : 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from'       : f'{SMS_SEND_PHONE_NUMBER}',
        "messages"   : [{"to": phone_number, }],
        'content'    : f'인증번호 [{sms_number}]',
    }

    response = requests.post(
        SMS_URL, data=json.dumps(data),
        headers=headers
    )

    if response.status_code == "202":
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

    return JsonResponse({"MESSAGE": "NAVER COULD NOT SEND SMS"}, status=400)


def kakao_access_token_required(func):
    @wraps(func)
    def decorated_function(self, request, *args, **kwargs):
        try:
            data               = json.loads(request.body)
            kakao_access_token = data['kakao_access_token']

            KAKAO_USER_INFO_REQUEST_URL = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                'Authorization' : f'Bearer {kakao_access_token}',
                'Content-type'  : 'application/x-www-form-urlencoded; charset=utf-8'
            }
            kakao_user_info_response = requests.get(KAKAO_USER_INFO_REQUEST_URL, headers = headers)

            # request.kakao_user_info = json.loads(kakao_user_info_response.text)
            request.kakao_user_info = kakao_user_info_response.json()

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY ERROR => " + e.args[0]}, status=400)

        return func(self, request, *args, **kwargs)
    return decorated_function

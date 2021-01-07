import json, requests
from functools import wraps

from django.http import JsonResponse


REGEX_PASSWORD = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{10,}$'  # 영문+숫자+특수문자 10자 이상
REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


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

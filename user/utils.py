import jwt
from functools import wraps

from django.http import JsonResponse

from my_settings import SECRET_KEY, ENCRYPTION_ALGORITHM
from user.models import User


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

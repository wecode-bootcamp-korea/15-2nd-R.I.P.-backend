import jwt
from datetime import timedelta, datetime

from django.views import View
from django.http  import JsonResponse

from ..models     import User, AccountType
from my_settings  import SECRET_KEY, ALGORITHM
from ..utils      import kakao_access_token_required


class KakaoSignIn(View):
    @kakao_access_token_required
    def post(self, request):
        try:
            kakao_user_info = request.kakao_user_info

            user = User.objects.get(email=kakao_user_info['kakao_account']['email'])
            if user.account_type.name == "kakao":
                access_token = jwt.encode({'id':user.email, 'exp': datetime.utcnow() + timedelta(hours=24 * 14)}, SECRET_KEY, ALGORITHM).decode('utf-8')
                return JsonResponse({"ACCESS_TOKEN" : access_token, 'NICKNAME' : user.nickname}, status=200)

            if user.account_type.name == "email":
                return JsonResponse({"MESSAGE": "EMAIL ACCOUNT EXISTS"}, status=400)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY ERROR => " + e.args[0]}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID USER"}, status=400)

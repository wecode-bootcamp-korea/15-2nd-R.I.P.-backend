import jwt
from datetime import timedelta, datetime

from django.views import View
from django.http  import JsonResponse

from user.models     import User, AccountType
from my_settings  import SECRET_KEY, ALGORITHM
from user.utils      import kakao_access_token_required


class KakaoSignUp(View):
    @kakao_access_token_required
    def post(self, request):
        try:
            kakao_user_info = request.kakao_user_info
            email_account_type = AccountType.objects.get(name="email")
            kakao_account_type = AccountType.objects.get(name="kakao")

            if User.objects.filter(account_type = email_account_type, email = kakao_user_info['kakao_account']['email']).exists():
                return JsonResponse({"MESSAGE": "KAKAO ACCOUNT EXISTS"}, status=400)

            if User.objects.filter(account_type = kakao_account_type, email=kakao_user_info['kakao_account']['email']).exists():
                return JsonResponse({"MESSAGE": "EMAIL ACCOUNT EXISTS"}, status=400)

            user = User.objects.create(
                social_login_id = kakao_user_info['id'],
                account_type_id = 2,
                email           = kakao_user_info['kakao_account']['email'],
                nickname        = kakao_user_info['properties']['nickname'],
                profile_image   = kakao_user_info['properties']['profile_image'],
            )
            access_token = jwt.encode({'id':user.email, 'exp': datetime.utcnow() + timedelta(hours=24 * 14)}, SECRET_KEY, ALGORITHM).decode('utf-8')
            return JsonResponse({"ACCESS_TOKEN" : access_token, 'NICKNAME' : user.nickname}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY ERROR => " + e.args[0]}, status=400)

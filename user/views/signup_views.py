import re,  json, bcrypt

from django.views import View
from django.http  import JsonResponse

from ..models     import Authentication, User
from ..utils      import REGEX_PASSWORD, REGEX_EMAIL


class SigupUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({"MESSAGE": "INVALID PASSWORD"}, status=400)

            if not re.match(REGEX_EMAIL, data['email']):
                return JsonResponse({"MESSAGE": "INVALID EMAIL"}, status=400)

            if User.objects.filter(email = data['email'], account_type_id = 1).exists():
                return JsonResponse({"MESSAGE" : "EMAIL ACCOUNT EXISTS"}, status=400)

            if User.objects.filter(email = data['email'], account_type_id = 2).exists():
                return JsonResponse({"MESSAGE" : "KAKAO ACCOUNT EXISTS"}, status=400)

            if Authentication.objects.filter(
                    phone_number     = data['phone_number'],
                    sms_number       = data['sms_number'],
                    is_authenticated = True,
            ).exists():

                hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                User.objects.create(
                    email           = data['email'],
                    nickname        = data['nickname'],
                    password        = hashed_pw,
                    phone_number    = data['phone_number'],
                    account_type_id = 1,
                )

                return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)

            return JsonResponse({"MESSAGE": "AUTHENTICATION FAIL"}, status=400)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + str(e.args[0])}, status=400)

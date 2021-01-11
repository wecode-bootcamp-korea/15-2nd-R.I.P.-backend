import json,  bcrypt, jwt
from datetime import timedelta, datetime

from django.views import View
from django.http  import JsonResponse

from ..models     import User
from my_settings  import SECRET_KEY, ALGORITHM


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id' : user.email,
                                           'exp': datetime.utcnow() + timedelta(hours=24 * 14)}, SECRET_KEY, ALGORITHM
                                          ).decode('utf-8')

                return JsonResponse({"MESSAGE"     : "SUCCESS",
                                     "ACCESS_TOKEN": access_token,
                                     'nickname'    : user.nickname}, status=200)

            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)

        except KeyError as e:
            return JsonResponse({'MESSAGE': 'KEY_ERROR => ' + str(e.args[0])}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
        except ValueError as e:
            return JsonResponse({'MESSAGE': 'ValueError => ' + str(e.args[0])}, status=400)

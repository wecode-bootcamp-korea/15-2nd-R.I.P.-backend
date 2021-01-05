import re, json
from datetime import timedelta, datetime
from random   import randint

from django.views import View
from django.http  import JsonResponse

from user.models     import Authentication
from user.utils      import REGEX_PHONE_NUMBER, send_sms



class SendSmsView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.match(REGEX_PHONE_NUMBER, data['phone_number']):
                return JsonResponse({"MESSAGE": "INVALID PHONE_NUMBER"}, status=400)

            sms_number = randint(100000, 1000000)

            authentication, flag             = Authentication.objects.get_or_create(phone_number=data['phone_number'])
            authentication.sms_number        = sms_number
            authentication.sms_request_count += 1
            authentication.save()

            send_sms(phone_number=data['phone_number'], sms_number=sms_number)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


class AuthenticateSmsView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.match(REGEX_PHONE_NUMBER, data['phone_number']):
                return JsonResponse({"MESSAGE": "INVALID PHONE_NUMBER"}, status=400)

            authentication = Authentication.objects.get(
                phone_number = data['phone_number'],
                sms_number   = data['sms_number'],
            )
            authentication.try_count += 1

            if datetime.now() - authentication.updated_at > timedelta(seconds = 60 * 5):
                authentication.save()
                return JsonResponse({"MESSAGE" : "TIMEOUT"}, status=400)

            authentication.is_authenticated = True
            authentication.save()
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY ERROR => " + e.args[0]}, status=400)
        except Authentication.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID ACCESS'}, status=401)

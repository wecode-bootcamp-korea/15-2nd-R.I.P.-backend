import json

from django.test  import Client
from django.test  import TestCase

from user.models import Authentication


class SmsSendViewTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_sms_request_success(self):
        phone_number = {
            'phone_number': "01047093556"  # sms를 받을 번호(실제로 발송됨)
        }
        response = self.client.post('/user/signup/sms_request', json.dumps(phone_number), content_type = 'application/json')

        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})
        self.assertEqual(response.status_code, 200)


    def test_sms_request_fail_with_poor_phone_number(self):
        poor_phone_number = {
            'phone_number' : "77711112222"
        }
        response = self.client.post('/user/signup/sms_request', json.dumps(poor_phone_number), content_type = 'application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID PHONE_NUMBER"})
        self.assertEqual(response.status_code, 400)


class AuthenticateSmsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Authentication(
            phone_number     = "01000000000",
            sms_number       = "123456",
            is_authenticated = False,
        ).save()


    def test_sms_authentication_success(self):
        sms_authentication = {
            'phone_number': "01000000000",
            'sms_number'  : "123456",
        }
        response = self.client.post('/user/signup/sms_authentication', json.dumps(sms_authentication), content_type = 'application/json')

        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})
        self.assertEqual(response.status_code, 200)


    def test_sms_authentication_fail_with_poor_phone_number(self):
        poor_phone_number = {
            'phone_number': "77711112222",
            'sms_number'  : "123456",
        }
        response = self.client.post('/user/signup/sms_request', json.dumps(poor_phone_number), content_type = 'application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID PHONE_NUMBER"})
        self.assertEqual(response.status_code, 400)


    def test_sms_authentication_fail_with_wrong_phone_number(self):
        wrong_phone_number = {
            'phone_number': "01077777777",
            'sms_number'  : "123456",
        }
        response = self.client.post('/user/signup/sms_authentication', json.dumps(wrong_phone_number), content_type = 'application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID ACCESS"})
        self.assertEqual(response.status_code, 401)

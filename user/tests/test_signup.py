import json

from django.test      import Client
from django.test      import TestCase

from user.models import Authentication, User, AccountType


class SignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountType(name='email').save() # 1
        AccountType(name='kakao').save() # 2

        Authentication(
            phone_number     = '01012345678',
            sms_number       = '123456',
            is_authenticated = True,
        ).save()


    def setUp(self):
        self.new_user = {
            'email'       : 'homer@homer.com',
            'password'    : '12345qwert!@#$%',
            'nickname'    : 'Homer Jay Simpson',
            'phone_number': '01012345678',
            'sms_number'  : '123456',
        }

        self.client = Client()

        self.email_account_type = AccountType.objects.get(name="email")
        self.kakao_account_type = AccountType.objects.get(name="kakao")



    def test_signup_success(self):

        response = self.client.post('/user/signup', json.dumps(self.new_user), content_type='application/json')

        self.assertEqual(response.status_code, 201)

        User.objects.all().delete()


    def test_signup_fail_with_poor_password(self):
        poor_password_user = {
            'email'       : 'homer@homer.com',
            'password'    : 'password',
            'nickname'    : 'Homer Jay Simpson',
            'phone_number': '01012345678',
            'sms_number'  : '123456',
        }
        response = self.client.post('/user/signup', json.dumps(poor_password_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID PASSWORD"})
        self.assertEqual(response.status_code, 400)


    def test_signup_fail_with_poor_email(self):
        poor_email_user = {
            'email'       : 'homer#homer.com',
            'password'    : '12345qwert!@#$%',
            'nickname'    : 'Homer Jay Simpson',
            'phone_number': '01012345678',
            'sms_number'  : '123456',
        }

        response = self.client.post('/user/signup', json.dumps(poor_email_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID EMAIL"})
        self.assertEqual(response.status_code, 400)


    def test_signup_fail_with_authentication_fail(self):
        authentication = Authentication.objects.get(phone_number = '01012345678')
        authentication.is_authenticated = False
        authentication.save()

        response = self.client.post('/user/signup', json.dumps(self.new_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "AUTHENTICATION FAIL"})
        self.assertEqual(response.status_code, 400)


    def test_signup_fail_with_email_duplication(self):
        Authentication(
            phone_number     = '01011112222',
            sms_number       = '111222',
            is_authenticated = True,
        ).save()

        User(
            email        = 'homer@homer.com',
            nickname     = 'King God Homer',
            password     = '12345qwert!@#$%',
            phone_number = '01011112222',
            account_type = self.email_account_type,
        ).save()

        response = self.client.post('/user/signup', json.dumps(self.new_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "EMAIL ACCOUNT EXISTS"})
        self.assertEqual(response.status_code, 400)


    def test_signup_fail_with_already_kakao_signed_up_with_email(self):
        Authentication(
            phone_number     = '01011112222',
            sms_number       = '111222',
            is_authenticated = True,
        ).save()

        User(
            email        = 'homer@homer.com',
            nickname     = 'King God Homer',
            password     = '12345qwert!@#$%',
            phone_number = '01011112222',
            account_type = self.kakao_account_type,
        ).save()

        response = self.client.post('/user/signup', json.dumps(self.new_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "KAKAO ACCOUNT EXISTS"})
        self.assertEqual(response.status_code, 400)



import json, bcrypt

from django.test  import Client
from django.test  import TestCase

from user.models  import User, AccountType


class SignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountType(name='email').save()
        AccountType(name='kakao').save()

        password = '12345qwert!@#$%'
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        email_account_type = AccountType.objects.get(name="email")

        User(
            email        = 'homer@homer.com',
            nickname     = 'King God Homer',
            password     = hashed_pw,
            phone_number = '01012345678',
            account_type = email_account_type
        ).save()


    def setUp(self):

        self.signin_user = {
            'email'   : 'homer@homer.com',
            'password': '12345qwert!@#$%',
        }

        self.client = Client()


    def test_signin_success(self):
        response = self.client.post('/user/signin', json.dumps(self.signin_user), content_type='application/json')

        self.assertEqual(response.status_code, 200)


    def test_signin_fail_with_no_account(self):
        account_not_matching_user = {
            'email'   : 'bart@bart.com',
            'password': '12345qwert!@#$%',
        }
        response = self.client.post('/user/signin', json.dumps(account_not_matching_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID_USER"})
        self.assertEqual(response.status_code, 400)


    def test_signin_fail_with_not_matching_password(self):
        password_not_matching_user = {
            'email'   : 'homer@homer.com',
            'password': 'password',
        }
        response = self.client.post('/user/signin', json.dumps(password_not_matching_user), content_type='application/json')

        self.assertEqual(response.json(), {"MESSAGE": "INVALID_USER"})
        self.assertEqual(response.status_code, 400)
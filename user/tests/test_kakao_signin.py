import json

from django.test    import TestCase,Client
from unittest.mock  import patch,MagicMock

from user.models import AccountType, User


class KakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountType(name='kakao').save()


    @patch('user.utils.requests')
    def test_kakao_sign_in(self, mock_request):
        class FakeKakaoResponse:
            def json(self):
                return {
                    "kakao_account":
                    {
                        "email": "homer_the_king@homer.com",
                    },
                }

        User(
            email = "homer_the_king@homer.com",
            social_login_id = "1234",
            nickname = "god homer",
            account_type = AccountType.objects.get(name="kakao"),
        ).save()

        kakao_access_token = {'kakao_access_token' : 123454321}

        mock_request.get = MagicMock(return_value = FakeKakaoResponse())

        response = Client().post('/user/kakao-signin', json.dumps(kakao_access_token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

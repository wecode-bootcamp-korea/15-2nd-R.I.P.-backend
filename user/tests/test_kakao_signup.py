import json

from django.test    import TestCase,Client
from unittest.mock  import patch,MagicMock

from user.models import AccountType


class KakaoSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountType(name='email').save()
        AccountType(name='kakao').save()


    @patch('user.utils.requests')
    def test_kakao_sign_up(self, mock_request):
        class FakeKakaoResponse:
            def json(self):
                return {
                    "id"           : "12345678",
                    "kakao_account":
                    {
                        "email": "homer_the_king@homer.com",
                    },
                    "properties":
                    {
                        "nickname"     : "homer the king",
                        "profile_image": "profile_image",
                    }
                }

        kakao_access_token = {'kakao_access_token' : 123454321}

        mock_request.get = MagicMock(return_value = FakeKakaoResponse())

        response = Client().post('/user/kakao-signup', json.dumps(kakao_access_token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

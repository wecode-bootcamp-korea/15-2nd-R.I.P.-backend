from django.urls import path
from .views.signin_views import SignInView
from .views.sms_authentication_views import SendSmsView, AuthenticateSmsView
from user.views.kakao_signup_views import KakaoSignUp


urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/signup/sms_request', SendSmsView.as_view()),
    path('/signup/sms_authentication', AuthenticateSmsView.as_view()),
    path('/kakao-signup', KakaoSignUp.as_view()),
]

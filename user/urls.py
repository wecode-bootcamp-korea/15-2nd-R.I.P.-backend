from django.urls                         import path
# from user.views.signup_views             import SigupUpView
from user.views.signin_views             import SignInView
from user.views.kakao_signup_views       import KakaoSignUp
from user.views.kakao_signin_views       import KakaoSignIn
from user.views.sms_authentication_views import SendSmsView, AuthenticateSmsView


urlpatterns = [
    # path('/signup', SigupUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/signup/sms_request', SendSmsView.as_view()),
    path('/signup/sms_authentication', AuthenticateSmsView.as_view()),
    path('/kakao-signup', KakaoSignUp.as_view()),
    path('/kakao-signin', KakaoSignIn.as_view()),
  ]
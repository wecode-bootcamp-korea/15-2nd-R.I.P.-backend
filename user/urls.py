from django.urls import path

from user.views.signup_views       import SigupUpView
from user.views.kakao_signin_views import KakaoSignIn


urlpatterns = [
    path('/signup', SigupUpView.as_view()),
    path('/kakao-signin', KakaoSignIn.as_view()),
]

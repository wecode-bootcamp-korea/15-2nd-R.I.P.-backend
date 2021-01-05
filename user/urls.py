from django.urls import path
from .views.signin_views import SignInView
from .views.sms_authentication_views import SendSmsView, AuthenticateSmsView


urlpatterns = [
    path('/signin', SignInView.as_view()),
    path('/signup/sms_request', SendSmsView.as_view()),
    path('/signup/sms_authentication', AuthenticateSmsView.as_view()),
]

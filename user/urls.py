from django.urls import path

from .views.signup_views import SigupUpView


urlpatterns = [
    path('/signup', SigupUpView.as_view()),
]

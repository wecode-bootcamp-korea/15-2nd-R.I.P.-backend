from django.urls import path
from .views.signin_views import SignInView


urlpatterns = [
    path('/signin', SignInView.as_view()),
]

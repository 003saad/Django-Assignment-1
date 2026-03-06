from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import StyledAuthenticationForm
from .views import activate_user, signup_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=StyledAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", activate_user, name="activate_user"),
]

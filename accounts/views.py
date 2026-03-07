# from django.contrib import messages
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from django.shortcuts import redirect, render
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from .forms import SignUpForm
# from .utils import assign_user_to_group


# def signup_view(request):
#     form = SignUpForm(request.POST or None)

#     if request.method == "POST" and form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()

#         assign_user_to_group(user, "Participant")

#         messages.success(
#             request,
#             "Account created successfully. Please check your email to activate your account.",
#         )
#         return redirect("login")

#     return render(request, "accounts/signup.html", {"form": form})


# def activate_user(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(
#             request, "Your account has been activated. You can now log in."
#         )
#         return redirect("login")

#     messages.error(request, "Activation link is invalid or expired.")
#     return redirect("signup")
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .utils import assign_user_to_group


def signup_view(request):
    form = SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        assign_user_to_group(user, "Participant")

        messages.success(
            request,
            "Account created successfully. Please check your email to activate your account.",
        )
        return redirect("login")

    return render(request, "accounts/signup.html", {"form": form})


def activate_user(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Your account has been activated. You can now log in."
        )
        return redirect("login")

    messages.error(request, "Activation link is invalid or expired.")
    return redirect("signup")

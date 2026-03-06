from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


input_class = (
    "w-full bg-[#0f1116] border border-white/10 rounded px-3 py-2 "
    "text-gray-100 placeholder-gray-500 focus:outline-none "
    "focus:ring-2 focus:ring-red-400/40"
)


class SignUpForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": input_class, "placeholder": "Username"})
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": input_class, "placeholder": "First name"}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": input_class, "placeholder": "Last name"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": input_class, "placeholder": "Email address"}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": input_class, "placeholder": "Password"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": input_class, "placeholder": "Confirm password"}
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()

        return user


class StyledAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": input_class, "placeholder": "Username"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": input_class, "placeholder": "Password"}
        )
    )

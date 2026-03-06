from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active and instance.email:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)

        activation_link = f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}/"

        message = render_to_string(
            "accounts/activation_email.txt",
            {
                "user": instance,
                "activation_link": activation_link,
            },
        )

        send_mail(
            subject="Activate your account",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        print("\n" + "=" * 80)
        print("ACTIVATION LINK:")
        print(activation_link)
        print("=" * 80 + "\n")

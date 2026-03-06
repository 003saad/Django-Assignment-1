from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Event


@receiver(m2m_changed, sender=Event.rsvps.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        users = User.objects.filter(pk__in=pk_set)

        for user in users:
            subject = f"RSVP Confirmation for {instance.name}"
            message = (
                f"Hello {user.first_name or user.username},\n\n"
                f"You have successfully RSVP’d for the event:\n\n"
                f"Event: {instance.name}\n"
                f"Date: {instance.date}\n"
                f"Time: {instance.time}\n"
                f"Location: {instance.location}\n\n"
                f"Thank you."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

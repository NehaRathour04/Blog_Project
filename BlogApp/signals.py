from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import transaction
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance=False, created=False, **kwargs):
    # print("Function being called")
    if created and (instance.email):
        def send():
            send_mail(subject="New Account Created",
                      message=f"You have successfully created account on our website with username {instance.username}",
                      from_email='4r.a.j.p.u.t2@gmail.com',
                      recipient_list=[instance.email],
                      fail_silently=False
                      )

        transaction.on_commit(send)
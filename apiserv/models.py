from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from pyfcm import FCMNotification
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    images = models.ImageField(
        upload_to='images/', default='images/no-img.jpg'
    )
    cat = models.CharField(max_length=50)
    venue = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    time = models.CharField(max_length=50)
    link = models.CharField(max_length=150)
    short_desc = models.CharField(max_length=80)
    def __str__(self):
        return self.name


class User(AbstractUser):
    CHOICES = ((0, "UNPAID"), (1, "PAID"), (2, "CREDIT"))
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    mem_type = models.IntegerField(choices=CHOICES, default=0)


'''
Untested Code
'''
@receiver(post_save, sender=Event)
def send_notification(sender, instance, created, **kwargs):
    push_service = FCMNotification(api_key=settings.FIREBASE_KEY)
    message_title = "Upcoming Event - CSI"
    message_body = instance.short_desc
    push_service.notify_topic_subscribers(topic_name="newevents", message_body=message_body)


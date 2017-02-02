from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.utils import timezone


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

    def __str__(self):
        return self.name


class User(AbstractUser):
    CHOICES = ((0, "UNPAID"), (1, "PAID"), (2, "CREDIT"))
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    mem_type = models.IntegerField(choices=CHOICES, default=0)


'''
@receiver(post_save, sender=Event)
def send_notification(sender, instance, created, **kwargs):

<FIREBASE INTEGRATION>
'''


# Create your models here.

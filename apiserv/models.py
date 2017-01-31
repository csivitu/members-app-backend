from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
	name = models.CharField(max_length=200)
	desc = models.TextField()
	images=models.TextField()
	cat=models.CharField(max_length=50)
	venue=models.CharField(max_length=50)
	date = models.DateTimeField(default=timezone.now)
	time=models.CharField(max_length=50)
	link=models.CharField(max_length=150)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='user')
	name=models.CharField(max_length=50,blank=True)
	phone = models.CharField(max_length=12,blank=True)
	mem_type=models.CharField(max_length=12,blank=True)
	
	def __str__(self):
		return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile=Profile(user=instance)
        profile.save()
	


# Create your models here.



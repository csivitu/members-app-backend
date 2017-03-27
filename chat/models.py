from django.db import models
from apiserv.models import User

# Create your models here.
class Chat(models.Model):
    started = models.DateTimeField('started', editable=False, auto_now_add=True)
    users = models.ManyToManyField(User)
    isActive=models.BooleanField(default=True)

    def add_message(self, user_from, message_body):
        message = Message(chat=self, user_from=user_from, message_body=message_body)
        message.save()
        return message

class ChatbotContext(models.Model):
    user=models.ForeignKey(User)
    context=models.TextField()
    time=models.DateTimeField('time',auto_now_add=True)

class CoreChatRequest(models.Model):
    member=models.ForeignKey(User)
    isActive=models.BooleanField(default=True)
    time=models.DateTimeField('time')

class Message(models.Model):
    timestamp = models.DateTimeField('timestamp', editable=False, auto_now_add=True)
    chat = models.ForeignKey(Chat)
    user_from = models.ForeignKey(User)
    message_body = models.TextField(max_length=2000)
from django.db import models
from apiserv.models import User

# Create your models here.

class Chat(models.Model):
    started = models.DateTimeField('started', editable=False, auto_now_add=True)
    users = models.ManyToManyField(User)
    isActive=models.BooleanField(default=True)

    @property
    def users_list(self):
        user_list = []
        for i in self.users.iterator():
            user_list.append(i.username)
        return user_list

    def add_message(self, user_from, message_body):
        message = Message.objects.create(chat=self, user_from=user_from, message_body=message_body)
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
    user_from = models.ForeignKey(User,related_name='user_frm')
    message_body = models.TextField(max_length=2000)

    @property
    def msg_from(self):
        return self.user_from.username
from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length= 30)
    last_name = models.CharField(max_length= 30)
    email = models.EmailField(unique= True)
    password = models.CharField(max_length= 128)
    profile_picture = models.ImageField(upload_to= 'profiles/', null= True, blank= True)
    is_online = models.BooleanField(default= False)
    last_seen = models.DateField(null= True, blank= True)

    def __str__(self):
        return f"{User.first_name} {User.last_name}"
    

class Messages(models.Model):
    sender = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'sent_messages')
    recipient = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'received_messages')
    content = models.CharField(200)
    timestamp_sent = models.DateTimeField(auto_now_add= True)
    conversation = models.ForeignKey('Conversation', on_delete= models.CASCADE, related_name= 'messages')


class Conversation(models.Model):
    participants = models.ManyToManyField('User')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
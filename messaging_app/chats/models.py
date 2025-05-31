from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    first_name = models.CharField(max_length= 30)
    last_name = models.CharField(max_length= 30)
    password = models.CharField(max_length= 128)
    profile_picture = models.ImageField(upload_to= 'profiles/', null= True, blank= True)
    phone_number = models.CharField(max_length= 15)
    is_online = models.BooleanField(default= False)
    last_seen = models.DateField(null= True, blank= True)

    def __str__(self):
        return f"{User.first_name} {User.last_name}"
    

class Messages(models.Model):
    message_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    sender = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'sent_messages')
    recipient = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'received_messages')
    message_body = models.CharField(200)
    sent_at = models.DateTimeField(auto_now_add= True)
    conversation = models.ForeignKey('Conversation', on_delete= models.CASCADE, related_name= 'messages')


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    participants = models.ManyToManyField('User')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
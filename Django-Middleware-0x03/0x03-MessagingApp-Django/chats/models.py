from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()


class User(models.Model):
    user_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    username = models.CharField(max_length= 30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length= 128)
    phone_number = models.CharField(max_length= 15)
    profile_picture = models.ImageField(upload_to= 'profiles/', null= True, blank= True)
    is_online = models.BooleanField(default= False)
    last_seen = models.DateField(null= True, blank= True)

    def __str__(self):
        return f"{User.first_name} {User.last_name}"
    

class Message(models.Model):
    message_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    sender = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'sent_messages')
    receiver = models.ForeignKey('User', on_delete= models.CASCADE, related_name= 'received_messages')
    message_body = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add= True)
    conversation = models.ForeignKey('Conversation', on_delete= models.CASCADE, related_name= 'conversations')


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
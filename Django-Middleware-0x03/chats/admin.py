from django.contrib import admin
from .models import Message, Conversation, User

@admin.register(User)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_id','username','email', 'phone_number', 'is_online', 'last_seen']
    
admin.register(Conversation)
admin.register(Message)
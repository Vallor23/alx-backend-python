from rest_framework import serializers
from .models import User, Messages, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name","email", "password", "phone_number", "profile_picture", "is_online", "last_seen"]
        
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ["message_id", "sender", "message_body","recipient", "sent_at", "conversation"]

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at","updated_at", "sent_at", "conversation"]
from rest_framework import serializers
from .models import User, Messages, Conversation


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source = 'username', read_only = True)
    class Meta:
        model = User
        fields = ["user_id", "username","email", "password", "phone_number", "profile_picture", "is_online", "last_seen"]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email field cannot be empty.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)
    receiver = UserSerializer(read_only = True)
    class Meta:
        model = Messages
        fields = ["message_id", "sender", "message_body", "receiver", "sent_at", "conversation"]
        read_only_fields = [ "sender", "receiver", "sent_at"]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("message_body field cannot be empty.")
        return value
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many = True, read_only = True)
    messages = UserSerializer(many = True, read_only = True)
    conversation_title = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at","updated_at", "sent_at", "messages"]

    def get_conversation_title(self, obj):
        return f"Conversation with {','.join([user.username for user in obj.participants.all()])}"
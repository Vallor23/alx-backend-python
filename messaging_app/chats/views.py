from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing conversations
    Filters by user_id query parameter or defaults to the authenticated user's conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter conversations by user_id from query parameters or the authenticated user.
        Ensures only the authenticated user's conversations are accessible.
        """
        user_id = self.request.query_params("user_id", None)
        if user_id is not None:
            try:
                user_id = int(user_id)
                # Ensure the requesting user can only filter by their own ID
                if user_id != self.request.user.id:
                    raise ValidationError("You can only filter by your own user ID.")
                return Conversation.objects.filter(participants__id = user_id)
            except:
                raise ValidationError("Invalid user_id: must be an integer.")
        #Optionally returnconversations based on the authenticated user
        return Conversation.objects.filter(participants = self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing messages
    Filters by conversation_id query parameter or defaults to messages in the authenticated user's conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params("conversation_id", None)
        if conversation_id is not None:
            try:
                conversation_id = int(conversation_id)
                # Check if the user is a participant in the conversation
                if not Conversation.objects.filter(id=conversation_id, participants__id = self.request.user).exists():
                    raise ValidationError("You are not a participant of this conversation")
                return Message.objects.filter(conversation__id = conversation_id)
            except ValueError:
                raise ValidationError("Invalid conversation_id: must be an integer.")
        # Default: return messages from all conversations the user is part of
        return(Message.objects.filter(conversation__participant = self.request.user))
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .pagination import MessagePagination


User = get_user_model()
# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing, retrieving, creating, updating, and deleting conversations.
    Filters by user_id query parameter or defaults to the authenticated user's conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Filter conversations by user_id from query parameters or the authenticated user.
        Ensures only the authenticated user's conversations are accessible.
        """
        user_id = self.request.query_params.get("user_id", None)
        if not self.request.user.is_authenticated:
            return Conversation.objects.none()
        if self.request.user.is_staff:  # Admins see all conversations
            return Conversation.objects.all()
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        """
        Create a new message with the authenticated user as the sender.
        Expects 'conversation' (conversation ID) and 'content' in the request data.
        """
        


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing messages
    Filters by conversation_id query parameter or defaults to messages in the authenticated user's conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipantOfConversation]

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
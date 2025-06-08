from django.shortcuts import render
from rest_framework import viewsets, status
from .permissions import IsParticipantOfConversation
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth import get_user_model
from .pagination import MessagePagination
from .filters import MessageFilter

# Create your views here.
User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing, retrieving, creating, updating, and deleting conversations.
    Filters by user_id query parameter or defaults to the authenticated user's conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipantOfConversation]
    
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
        
        # if username:
        #     try:
        #         user = User.objects.get(username=username)
        #     except User.DoesNotExist:
        #         raise NotFound(detail="User not found.")
        #         # user_id = int(user_id)
        #         # # Ensure the requesting user can only filter by their own ID
        #         # if user_id != self.request.user.id:
        #         #     raise ValidationError("You can only filter by your own user ID.", code= status.HTTP_403_FORBIDDEN)
        #     return Conversation.objects.filter(participants = username)
        #     # except:
        #     #     raise ValidationError("Invalid user_id: must be an integer.", code= status.HTTP_400_BAD_REQUEST)
        # #Optionally returnconversations based on the authenticated user
        # return Conversation.objects.filter(participants = self.request.user)
    
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
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipantOfConversation]
    pagination_classes = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

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
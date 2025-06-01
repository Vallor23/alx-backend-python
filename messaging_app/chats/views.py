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
    

# class MessageViewSet:
from rest_framework import permissions
from .models import Conversation, Message

class  IsParticipantOfConversation(permissions.BasePermission): 
    """
    Permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # obj here is a Conversation instance
        return request.user in obj.partcipants.all()
    
class  IsParticipantOfConversation(permissions.BasePermission): 
    """
    Allow only authenticated users who are participants in the conversation
    to send, view, update, and delete messages related to that conversation.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False
            
    
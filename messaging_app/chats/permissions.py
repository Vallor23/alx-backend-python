from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
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
            # allow access for viewing only if the user is a participant in the related conversation
            if request.method in SAFE_METHODS:
                return obj.conversation.participants.filter(id=request.user.id).exists()
            # sender of the message to be able to edit/delete
            elif request.method in ['PUT', 'PATCH', 'DELETE']:
                return obj.sender == request.user
        return False
            
    
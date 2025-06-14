from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from models import Message
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    request.user.delete()
    return HttpResponse("User deleted!")

@login_required
def get_message(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver')
    return [f"To {msg.receiver.username} : {msg.content}" for msg in messages]

def get_message_replies(request, pk):
    try:
        message = Message.objects.prefetch_related('replies').get(id=pk)  # 'replies' is the related_name on the ForeignKey - parent_message
        return [
            f"Replies to '{message.content}' : {reply.content}"
            for reply in message.replies.all()
        ] 
    except Message.DoesNotExist:
        return []
    
def get_unread_messages(request):
    unread_messages = Message.unread.filter(receiver=request.user).only('is_read')
    message_ids = [{msg.id} for msg in unread_messages]
    return f"Unread Messages : {message_ids}"

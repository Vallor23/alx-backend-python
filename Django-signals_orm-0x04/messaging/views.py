from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from models import Message
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    request.user.delete()
    return HttpResponse("User deleted!")

@login_required
@cache_page(60 * 1)
def get_message(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver')
    data = [
        {"to": msg.receiver.username, "content": msg.content}
        for msg in messages
    ]
    return JsonResponse(data, safe=False)

def get_unread_messages(request):
    messages =  Message.unread.unread_for_user(request.user)
    return [f"Message ID: {msg.id}" for msg in messages]
    
# Implement a recursive function to fetch all nested replies
def  get_threaded_replies(message, depth=0):
    indent = "_" * depth  # Indent replies for clarity
    output = [f"{indent} {message.content}"]

    for reply in message.replies.all().order_by('timestamp'):
        output += get_threaded_replies(reply, depth + 1)  # recurse
    return output

# view that uses get_message_threaded_replies func
def display_thread(request, pk):
    try:
        parent_message = Message.objects.prefetch_related('replies').get(id=pk)  # 'replies' is the related_name on the ForeignKey - parent_message
        thread = get_threaded_replies(parent_message)
        return HttpResponse("<br>".join(thread))
    except Message.DoesNotExist:
        return HttpResponse("Message not found")
    
def get_unread_messages(request):
    unread_messages = Message.unread.filter(receiver=request.user).only('is_read')
    message_ids =",".join([{msg.id} for msg in unread_messages])
    return f"Unread Messages : {message_ids}"

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # New field to link a reply to the message it's replying to
    parent_message = models.ForeignKey(
        'self',   # points to *another* Message
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(default='Message', max_length=50)

    def __str__(self):
        return f"Notification for{self.user.username} - {self.message}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Edit history for {self.message.id} edited at {self.edited_at}"
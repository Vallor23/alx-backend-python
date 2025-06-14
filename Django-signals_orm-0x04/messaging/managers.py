from django.db import models

# Custom ORM Manager for Unread messages
class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)
    
    def unread_for_user(self, user):
        return self.filter(receiver=user)
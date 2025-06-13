from django.db.models.signals import post_save, pre_save, post_delete 
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user = instance.receiver,
            message = instance
        )

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.id:
        try:
            old_message = Message.objects.get(id=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message = old_message,
                    old_content = old_message.content
                )
                instance.edited = True

        except Message.DoesNotExist:
            pass

@receiver(post_delete , sender=User)
def clean_up(sender, instance, **kwargs):
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # Delete notifications related to user
    instance.notifications.all().delete()
    # To delete all MessageHistory related to this user's messages:
    MessageHistory.objects.filter(message_sender=instance).delete()
    MessageHistory.objects.filter(message_receiver=instance).delete()
    
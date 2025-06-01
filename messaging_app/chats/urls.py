from django.urls import include, path
from rest_framework import routers
from chats.views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

app_name = 'chats'

url_patterns = [
    path('', include(router.urls))
]
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers
from chats.views import ConversationViewSet, MessageViewSet

# Base router for conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversation
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='converstaion')
nested_router.register(r'messages', MessageViewSet, basename='message')

app_name = 'chats'

url_patterns = [
    path('', include(router.urls))
]
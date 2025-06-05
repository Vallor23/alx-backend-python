from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

# Base router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversation
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

app_name = 'chats'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
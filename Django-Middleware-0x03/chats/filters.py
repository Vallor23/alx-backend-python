import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.filterset):
    #Fillter messages based on sender username
    
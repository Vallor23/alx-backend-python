from .models import Message
from django_filters import rest_framework as filters
from django.contrib.auth.models import User

class MessageFilter(filters.filterset):
    #Filtering by conversation participants
    participants = filters.ModelMultipleChoiceField(
        field_name = 'conversation__participant',
        query_set=User.objects.all(),
        conjoined=True  # Requires all listed participants
    )
    # Filter by timestamps
    created_at__gte = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model: Message
        fields = ['participants', 'created_at__gte', 'created_at__lte']
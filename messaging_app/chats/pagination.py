from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size =20  # Default number of messages per page
    page_size_query_params = 'page_size'
    max_page_size = 100
    
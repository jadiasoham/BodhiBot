from rest_framework.pagination import CursorPagination
from django.conf import settings

class ChatCursorPagination(CursorPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
    ordering = '-timestamp'
    cursor_query_param = 'cursor'

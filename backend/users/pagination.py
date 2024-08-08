from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Кастомная пагинация страниц."""

    page_size = settings.PAGE_SIZE_PAGINATION
    page_size_query_param = "limit"

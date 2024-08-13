from rest_framework.pagination import PageNumberPagination
class CustomBlogPAgination(PageNumberPagination):
    page_size=3
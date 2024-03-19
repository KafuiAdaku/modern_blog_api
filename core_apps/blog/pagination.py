from rest_framework.pagination import PageNumberPagination


class BlogPagination(PageNumberPagination):
    """Custom pagination for blog posts"""
    page_size = 5

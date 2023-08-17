from rest_framework.pagination import PageNumberPagination


class ViewsPaginator(PageNumberPagination):
    page_size = 10


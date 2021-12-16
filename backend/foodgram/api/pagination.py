from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    page_size = 6


class LimitPageNumberPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'limit'

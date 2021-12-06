from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    page_size = 6


class FollowPagination(PageNumberPagination):
    page_size = 6

from api.pagination import CustomPagination
from api.serializers import FollowSerializer
from django.contrib.auth import get_user_model
from djoser import views
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import Follow

User = get_user_model()


class FollowViewSet(views.UserViewSet):
    pagination_class = CustomPagination

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(follow)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        if user == following:
            return response.Response('Нельзя подписаться на себя',
                                     status=status.HTTP_400_BAD_REQUEST)
        elif Follow.objects.filter(user=user,
                                   following=following).exists():
            return response.Response('Вы уже подписаны на этого автора',
                                     status=status.HTTP_400_BAD_REQUEST)
        obj = Follow.objects.create(user=user, following=following)
        serializer = FollowSerializer(obj)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        Follow.objects.filter(user=user, following=following).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

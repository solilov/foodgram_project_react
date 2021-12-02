from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import FollowSerializer
from users.models import Follow


User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

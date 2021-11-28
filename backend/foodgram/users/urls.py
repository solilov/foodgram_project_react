from django.urls import include, path
from djoser import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
]

from django.urls import path
from . import views 
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('myprofile/', views.my_profile, name='myprofile'),
    path('profile/<str:user>/', views.other_profile, name='profile'),
    path('postview/', views.post_view, name='post_view'),
    path('myposts/', views.my_post_view, name='post_view'),
    path('otherposts/<str:user>/', views.other_post_view, name='post_view'),
    path('like/<int:pk>/', views.like_post, name='like'),
    path('follow/<int:pk>/', views.follow_unfollow_post, name='follow'),
    path('search/', views.search, name='search'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('image_upload/', post_test, name='image_upload'),
    path('upload/', views.upload, name='upload'),
    path('register/', views.register, name='register'),
    path('comments/<int:pk>/', CommentView.as_view()),
    path("", views.chatPage, name="chat-page"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


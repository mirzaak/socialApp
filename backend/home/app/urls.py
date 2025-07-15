from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, ProfileView, UserProfileView, PostListCreateView,
    UserPostsView, PostDetailView, LikePostView, CommentCreateView,
    FollowUserView, SearchUsersView, ExploreView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', ProfileView.as_view(), name='my-profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<str:username>/follow/', FollowUserView.as_view(), name='follow-user'),
    
    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/comment/', CommentCreateView.as_view(), name='create-comment'),
    path('posts/user/<str:username>/', UserPostsView.as_view(), name='user-posts'),
    path('posts/my/', UserPostsView.as_view(), name='my-posts'),
    
    # Explore & Search
    path('explore/', ExploreView.as_view(), name='explore'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
]
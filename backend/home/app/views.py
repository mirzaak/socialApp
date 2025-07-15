from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Profile, Post, Comment
from .serializers import (
    UserSerializer, ProfileSerializer, PostSerializer,
    CommentSerializer, RegisterSerializer, CreatePostSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Add this line!

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        print("Profile update request data:", request.data)
        print("Profile update request files:", request.FILES)
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            print("Profile updated successfully:", serializer.data)
            return Response(serializer.data)
        else:
            print("Profile update validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.profile


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        following_users = self.request.user.following.all().values_list('user', flat=True)
        return Post.objects.filter(
            user__in=list(following_users) + [self.request.user.id]
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        print("Creating post with data:", self.request.data)  # Debug line
        print("Files:", self.request.FILES)  # Debug line
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("POST request data:", request.data)  # Debug line
        print("POST request files:", request.FILES)  # Debug line
        return super().create(request, *args, **kwargs)


class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
            return Post.objects.filter(user=user)
        return Post.objects.filter(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({'liked': liked, 'likes_count': post.likes_count})


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = user_to_follow.profile
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
            following = False
        else:
            profile.followers.add(request.user)
            following = True
        
        return Response({'following': following, 'followers_count': profile.followers_count})


class SearchUsersView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'bio']

    def get_queryset(self):
        return Profile.objects.all()


class ExploreView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Get popular posts (most liked in the last 7 days)
        from datetime import datetime, timedelta
        last_week = datetime.now() - timedelta(days=7)
        return Post.objects.filter(
            created_at__gte=last_week
        ).order_by('-likes')[:20]
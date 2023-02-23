from rest_framework import generics, viewsets, status
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from .serializers import UserSerializer, PostSerializer, ProfileSerializer, CommentSerializer, PublicUserSerializer, CreatePostSerializer, RegisterSerializer, CreateCommentSerializer
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

class CreateProfile(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        posts = Profile.objects.get(user=self.request.user)
        posts_data = ProfileSerializer(posts).data
        return Response(data=posts_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.save()
            Profile.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


my_profile = CreateProfile.as_view()

class OtherProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    def get(self, *args, **kwargs):
        post_id = kwargs.get('user')
        posts = Profile.objects.get(user__username=post_id)
        posts_data = ProfileSerializer(posts).data
        return Response(data=posts_data, status=status.HTTP_200_OK)

other_profile = OtherProfile.as_view()

class PostView(APIView):
    def get(self, *args, **kwargs):
            my_profile = Profile.objects.get(user=self.request.user)
            my_posts = Q(profile=my_profile)
            posts = Q(profile__followers=self.request.user)
            all_posts = Post.objects.filter(my_posts & posts)
            posts_data = PostSerializer(all_posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CreatePostSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, data=request.data, profile=request.user.profile)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post = Post.objects.get(id=post_id)
            if post.user.id == request.user.id:
                post.delete()
                return Response({'msg': 'Post deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)

post_view = PostView.as_view()

class MyPostView(APIView):
    def get(self, *args, **kwargs):
            posts = Post.objects.filter(user=self.request.user)
            posts_data = PostSerializer(posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

my_post_view = MyPostView.as_view()

class OtherPostView(APIView):
    def get(self, *args, **kwargs):
            profile_id = kwargs.get('user')
            this_profile = Profile.objects.get(user__username=profile_id)
            posts = Post.objects.filter(profile=this_profile)
            posts_data = PostSerializer(posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

other_post_view = OtherPostView.as_view()

class LikePost(APIView):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        try:
            post = Post.objects.get(id=post_id)
            liked = post.likes.filter(id=request.user.id).exists()

            if liked:
                post.likes.remove(request.user.id)
                return Response(PostSerializer(post).data , status=status.HTTP_200_OK)
            else:
                post.likes.add(request.user.id)
                post.save()
                return Response(PostSerializer(post).data , status=status.HTTP_200_OK)
        except:
            return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)

like_post = LikePost.as_view()

class CommentView(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request,  *args, **kwargs):
        serializer = CreateCommentSerializer(data=request.data)
        post_pk = kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        if serializer.is_valid():
            serializer.save()
            d = serializer.save()
            post.comments.add(d)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

comment_post = CommentView.as_view()

class FollowUnfollow(APIView):
    def post(self, request, *args, **kwargs):
        profile_id = kwargs.get('pk')
        try:
            my_profile = Profile.objects.get(user=self.request.user)
            profile = Profile.objects.get(id=profile_id)
            followed = profile.followers.filter(id=request.user.id).exists()

            if followed:
                my_profile.followings.remove(request.user.id)
                profile.followers.remove(request.user.id)
                return Response(ProfileSerializer(profile).data , status=status.HTTP_200_OK)
            else:
                my_profile.followings.add(profile.id)
                profile.followers.add(request.user.id)
                profile.save()
                return Response(ProfileSerializer(profile).data , status=status.HTTP_200_OK)
        except:
            return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)

follow_unfollow_post = FollowUnfollow.as_view()

class UserListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

search = UserListView.as_view()

class PostTest(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, *args, **kwargs):
            my_profile = Profile.objects.get(user=self.request.user)
            my_posts = Q(user=self.request.user)
            posts = Q(profile__followers=self.request.user)
            all_posts = Post.objects.filter(Q(my_posts) | Q(posts))
            posts_data = PostSerializer(all_posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

post_test = PostTest.as_view()

def upload(request):
    if request.FILES:
        form = PostSerializer(request.POST, request.FILES)

        if form.is_valid():
            form.save()
    
    return ({'success': True})

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            return Response({'success':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

register = RegisterAPI.as_view()

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)
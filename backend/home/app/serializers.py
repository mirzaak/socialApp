from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from rest_framework.fields import CurrentUserDefault
from .models import Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "password",
        ]


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "pk",
            "user",
            "image",
            "followers",
            "followings",
        ]


class GetCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "user", "text", "date"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "user", "text", "date"]


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "user", "text", "date"]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=CurrentUserDefault())
    profilefull = ProfileSerializer(source="user.profile", read_only=True)
    comments = GetCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "pk",
            "user",
            "image",
            "caption",
            "likes",
            "isLikedByMe",
            "profile",
            "profilefull",
            "comments",
        ]


class CreatePostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = [
            "pk",
            "user",
            "image",
            "caption",
            "likes",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user

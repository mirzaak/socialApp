from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Post, Profile, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)  # Make image field explicit

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'bio', 'followers_count', 'following_count', 'is_following']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

    def update(self, instance, validated_data):
        print("ProfileSerializer update called with:", validated_data)
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'user', 'text', 'created_at']
        read_only_fields = ['pk', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    profilefull = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['pk', 'user', 'profilefull', 'image', 'caption', 'likes', 'likes_count', 
                  'comments_count', 'is_liked', 'comments', 'created_at']
        read_only_fields = ['pk', 'created_at']

    def get_profilefull(self, obj):
        """Return user profile data"""
        try:
            profile = obj.user.profile
            return {
                'image': profile.image.url if profile.image else None,
                'bio': profile.bio,
            }
        except Profile.DoesNotExist:
            return {'image': None, 'bio': ''}

    def get_likes(self, obj):
        """Return array of user IDs who liked this post"""
        return list(obj.likes.values_list('id', flat=True))

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_image(self, obj):
        """Return the full image URL or None"""
        if obj.image and obj.image.name:
            try:
                # This will return the correct URL with the actual filename
                return obj.image.url
            except ValueError:
                # Handle case where file doesn't exist
                return None
        return None


class CreatePostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    caption = serializers.CharField(required=False)
    
    class Meta:
        model = Post
        fields = ['image', 'caption']
        
    def validate(self, attrs):
        # Debug print
        print("CreatePostSerializer validate called with:", attrs)
        
        # Ensure at least image or caption is provided
        if not attrs.get('image') and not attrs.get('caption'):
            raise serializers.ValidationError("Either image or caption must be provided")
        return attrs

    def create(self, validated_data):
        print("CreatePostSerializer create called with:", validated_data)
        return super().create(validated_data)
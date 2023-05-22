from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/", default="media/default_user.png")
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    followings = models.ManyToManyField(User, related_name="followings", blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/")
    caption = models.CharField(max_length=120)
    likes = models.ManyToManyField(User, related_name="comments", blank=True)
    isLikedByMe = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    comments = models.ManyToManyField(Comment, related_name="comments", blank=True)

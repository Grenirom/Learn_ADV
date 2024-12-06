from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to="posts-images/")
    tag = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    def increment_views_count(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return f"{self.title}"

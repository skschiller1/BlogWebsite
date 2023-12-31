from django.db import models
from myblogsite import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("category", related_name="posts")
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

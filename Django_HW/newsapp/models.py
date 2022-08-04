from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=128, default="null", unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.name.title()

    def add_user(self, user):
        self.subscribers.add(user)

class Post(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory', related_name='news')
    type = models.CharField(max_length=50, choices=[('article', 'article'),('news', 'news')])
    post_time_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name.title()}: {self.description[:100]}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_datetime = models.DateTimeField(auto_now_add=True)


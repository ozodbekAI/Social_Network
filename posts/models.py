from django.db import models

from config import settings

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=80)


    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)


class LikeDislikes(models.Model):
    LIKE = 1 
    DISLIKE = -1

    VOTE_CHOICES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    def __str__(self):
        return f"{self.post.title} - {self.user.username} - {self.get_vote_display()}"
    
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=55, unique=True)
    phone  = models.CharField(max_length=13)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=24)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.username
    

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def accept(self):
        self.is_accepted = True
        self.save()

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'
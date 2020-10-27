from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted_user")
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="likes",null=True)
    
    def likes_count(self):
        return self.likes.count()
        
class Follow(models.Model):
    followers = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_follow')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following_user')

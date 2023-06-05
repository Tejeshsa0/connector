from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


# Create your models here.

#user model
class Profile(models.Model):
    username = models.CharField((""),max_length=29)
    number = models.CharField((""), max_length=10)
    profileimg = models.ImageField(upload_to= 'profileimgs', default='blankimg.png')
    email = models.EmailField((""), max_length=254) 

    def __str__(self):
        return self.username
    
#Post Model
class Post(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4)
    user= models.CharField(max_length=10)
    image = models.ImageField(upload_to = 'post_images')
    caption = models.TextField()
    privacy = models.CharField(max_length=20, default='public')
    username = models.CharField( max_length=100, default= "Username")

    def __str__(self):
        return self.user

#Connect model
class Connect(models.Model):
    user= models.CharField(max_length=10)
    connect= models.CharField(max_length=10)

    def __str__(self):
        return self.user
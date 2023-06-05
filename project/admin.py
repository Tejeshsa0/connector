from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, Connect

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Connect)
from django.contrib import admin
from .models import Profile,AddPost,LikePost,FollowerCount

# Register your models here.

admin.site.register(Profile)
admin.site.register(AddPost)
admin.site.register(LikePost)
admin.site.register(FollowerCount)
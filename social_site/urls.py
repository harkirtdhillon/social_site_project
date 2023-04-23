"""
URL configuration for social_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from social_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup',views.signup, name='signup'),
    path('login',views.Login,name='Login'),
    path('logout',views.Logout,name='Logout'),
    path('settings',views.settings,name='settings'),
    path('search',views.search,name='search'),
    path('addpost',views.upload,name='AddPost'),
    path('like-post',views.like_post,name='like-post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow',views.follow,name='follow')
]
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)




from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,AddPost,LikePost,FollowerCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.
@login_required(login_url='Login')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following_list=[]
    feed =[]

    user_following_=FollowerCount.objects.filter(follower=request.user.username)

    for users in user_following_:
        user_following_list.append(users.user)

    for usernames in user_following_:
        feed_lists=AddPost.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list =list(chain(*feed))


    all_users=User.objects.all()
    user_following_all=[]

    for user in user_following_:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    
    username_profile=[]
    username_profile_list=[]
    
    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_pro_list = list(chain(*username_profile_list))

    return render(request,'home.html',{'posts':feed_list,'user_profile':user_profile,'suggestions_username_pro_list':suggestions_username_pro_list[ :4]})

@login_required(login_url='Login')
def upload(request):
    if request.method == 'POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=AddPost.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='Login')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post = AddPost.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='Login')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image= user_profile.profileimg
            name=request.POST['name']
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg = image
            user_profile.user_name=name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name= request.POST['name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.user_name=name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request,'settings.html',{'user_profile':user_profile})

@login_required(login_url='Login')
def search(request):
    if request.method == 'POST':
        username= request.POST['username']
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list=[]

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'username_profile_list':username_profile_list})

@login_required(login_url='Login')
def follow(request):
    if request.method == 'POST':
        follower= request.POST['follower']
        user= request.POST['user']

        if FollowerCount.objects.filter(follower = follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowerCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='Login')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts = AddPost.objects.filter(user=pk)
    user_post_length= len(user_posts)
    follower = request.user.username
    user =pk

    if FollowerCount.objects.filter(follower=follower,user=user).first():
        button_text = 'following'
        btn_cls='btn btn-white text-black border border-2   mb-3'
    else:
        button_text = 'follow'
        btn_cls='btn btn-primary mb-3 '

    user_followers = len(FollowerCount.objects.filter(user=pk))
    user_following = len(FollowerCount.objects.filter(follower=pk))



    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'btn_cls':btn_cls,
        'user_following':user_following,
        'user_followers':user_followers,
    }

    return render(request,'profile.html',context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()

                

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('Login')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup')        
    else:
        return render(request, 'signup.html')
    
def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'User Not Found')
            return redirect('Login')
    else:
        return render(request, 'login.html')
    
@login_required(login_url='Login')
def Logout(request):
    auth.logout(request)
    return redirect('Login')
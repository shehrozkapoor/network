from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User,Post,Follow
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# index method checking if the user is logged in then 
# it will display post that user are following else all the post will be shown
def index(request):
    if request.user.is_authenticated:
        try:  
            follows = Follow.objects.filter(followers=request.user)
        except ObjectDoesNotExist:
            return render(request, "network/following_users.html")
        posts = Post.objects.all().order_by('id').reverse()
        posted = []
        for p in posts:
            for follower in follows:
                if follower.following == p.user:
                    posted.append(p)
        paginator = Paginator(posted, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {'page_obj': page_obj})
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'page_obj': page_obj})
# save post method is saving the post to django model
def save_post(request):
    if request.method == "POST":
        text = request.POST["post_text"]
        post = Post(user=request.user,text=text)
        post.save()
    return HttpResponseRedirect(reverse('index'))
# this is the login request method
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# logout request method 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("all_posts"))

#  register a new user request method 
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
# user profile will dispaly all it's own posts
def user_profile(request):
    posts = Post.objects.filter(user=request.user).order_by('id').reverse()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
      followers = Follow.objects.filter(following=request.user).count()
    except ObjectDoesNotExist:
        followers =0
    try:
        followings = Follow.objects.filter(followers=request.user).count()
    except ObjectDoesNotExist:
        followings = 0
    return render(request,"network/user_profile.html",{"page_obj":page_obj,"followers":followers,"followings":followings})
# all post will display all the post that are saved in database in reverse chronologinal 
def all_posts(request):
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/all_post.html",{"page_obj":page_obj})
# spec profile will display the if the user click on someone else 
# post to follow or unfollow and display all the post of requested user
def spec_profile(request,username):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    if request.user.username == username:
        return HttpResponseRedirect(reverse('user_profile'))
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        follow = Follow.objects.get(followers=request.user,following=user)
        unfollow = "unfollow"
    except ObjectDoesNotExist:
        unfollow = "follow"

    return render(request,'network/specific_profile.html',{"page_obj":page_obj,"username":username,"follow":unfollow})
# this will take the follow or unfollow request from the signed in user
def follow_unfollow(request,username):
    user1 = User.objects.get(username=request.user.username)
    user2 = User.objects.get(username=username)
    follow = Follow.objects.filter(followers=user1,following=user2)
    if follow:
        follow.delete()
        return HttpResponseRedirect(reverse('spec_profile',args=[username]))
    follow = Follow(followers=user1,following=user2)
    follow.save()
    return HttpResponseRedirect(reverse('spec_profile',args=[username]))
    
# following post will display the all the users post whom the request user is followings
def followings_posts(request):
    try:  
        follows = Follow.objects.filter(followers=request.user)
    except ObjectDoesNotExist:
        return render(request, "network/following_users.html")
    posts = Post.objects.all().order_by('id').reverse()
    posted = []
    for p in posts:
        for follower in follows:
            if follower.following == p.user:
                posted.append(p)
    paginator = Paginator(posted, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following_user.html", {'page_obj': page_obj})
# this is an api which will edit the post and send the JSON response to the request
@csrf_exempt
def edit_btn(request,id):
    post = Post.objects.get(id=id)
    if request.method == "GET":
        return JsonResponse(
            {"id":post.id,
            "text":post.text,
            }
        )
    elif request.method == "PUT":
        data = json.loads(request.body)
        post.text = data["content"]
        post.save()
        return JsonResponse({"message":"succesfull"})
    else:
        return JsonResponse({"error":"GET oR PUT request required"})
# this is an api which will call from javascript fecth function 
# if the user is liked then it will unlike the post else like the post
@csrf_exempt
def likes(request,id):
    post = Post.objects.get(pk=id)
    if request.method == "GET":
        if request.user in post.likes.all():
            return JsonResponse({"message":"liked"})
        else:
            return JsonResponse({"message":"notliked"})
    elif request.method == "PUT":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            status = "liked_removed"
        else:
            post.likes.add(request.user)
            status = "liked_succesful"
        post.save()
        return JsonResponse({"message":status})
    else:
        return JsonResponse({"error":"PUT request required"})
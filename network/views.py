from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.utils import timezone

from .models import User, Post, Follow


def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/register.html")


@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not content:
            return JsonResponse({"error": "Content cannot be empty"}, status=400)

        post = Post.objects.create(user=request.user, content=content, timestamp=timezone.now())
        profile_url = reverse('profile', args=[post.user.username])

        return JsonResponse({
            "post_id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%b %d, %Y %H:%M"),
            "profile_url": profile_url
        })

    return JsonResponse({"error": "POST request required."}, status=400)


@login_required
@csrf_exempt
def edit_post(request, post_id):
    """
    Endpoint do edycji własnego posta.
    """
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return JsonResponse({"error": "You cannot edit this post."}, status=403)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_content = data.get("content", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not new_content:
            return JsonResponse({"error": "Content cannot be empty."}, status=400)

        post.content = new_content
        post.save()

        return JsonResponse({
            "message": "Post updated successfully.",
            "content": post.content,
            "timestamp": post.timestamp.strftime("%b %d, %Y %H:%M")
        })

    return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def following(request):
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts_list = Post.objects.filter(user__in=followed_users).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(user=profile_user).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


@login_required
def follow(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.user == user_to_follow:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    followers_count = Follow.objects.filter(following=user_to_follow).count()

    return JsonResponse({
        "message": f"You are now following {user_to_follow.username}.",
        "followers_count": followers_count,
        "is_following": True,
    })


@login_required
def unfollow(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.user == user_to_unfollow:
        return JsonResponse({"error": "You cannot unfollow yourself."}, status=400)

    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    followers_count = Follow.objects.filter(following=user_to_unfollow).count()

    return JsonResponse({
        "message": f"You have unfollowed {user_to_unfollow.username}.",
        "followers_count": followers_count,
        "is_following": False,
    })


# -----------------------------------------------------
#   ★★★ LIKE / UNLIKE endpoint (DODANE)
# -----------------------------------------------------
@login_required
@csrf_exempt
def toggle_like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    post = get_object_or_404(Post, id=post_id)

    # Sprawdzamy czy użytkownik już polubił
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    return JsonResponse({
        "liked": is_liked,
        "total_likes": post.likes.count()
    })

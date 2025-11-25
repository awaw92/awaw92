from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post/", views.new_post, name="new_post"),  # URL dla tworzenia postów
    path("following/", views.following, name="following"),  # NOWY URL dla zakładki Following
    path("profile/<str:username>/", views.profile, name="profile"),  # URL profilu
    path("follow/<int:user_id>/", views.follow, name="follow"),  # URL do śledzenia użytkownika
    path("unfollow/<int:user_id>/", views.unfollow, name="unfollow"),  # URL do przestania śledzenia użytkownika
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),

    # ★★★ NOWY URL do Like/Unlike
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]

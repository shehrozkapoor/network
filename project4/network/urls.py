
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save_post",views.save_post,name ="save_post"),
    path("user_profile",views.user_profile,name="user_profile"),
    path('all_posts',views.all_posts,name='all_posts'),
    path('spec_profile/<username>',views.spec_profile,name="spec_profile"),
    path('follow_unfollow/<username>',views.follow_unfollow,name="follow_unfollow"),
    path('followings_posts',views.followings_posts,name='followings_posts'),
    # api_routes!!!!
    path('edit_post/<id>',views.edit_btn,name="edit_post"),
    path('liked/<id>',views.likes,name="liked")
]

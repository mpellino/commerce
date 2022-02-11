from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("listing_add", views.listing_add, name="listing_add"),
    path("<int:listing_id>/comment_add", views.comment_add, name="comment_add"),
    path("<int:listing_id>/bid_add", views.bid_add, name="bid_add"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id/wishlist_add>", views.wishlist_add, name="wishlist_add")
]

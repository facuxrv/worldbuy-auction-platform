from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("choosecategories", views.choose_categories, name="choose_categories"),
]
# The above code defines the URL patterns for the auctions app, mapping URLs to their corresponding view functions.
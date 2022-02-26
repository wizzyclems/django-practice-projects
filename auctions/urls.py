from django.conf.urls import url
from django.urls import path

from django.conf.urls.static import static

from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings", views.index, name="index"),
    path("listings/<int:list_id>", views.listing_detail, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addListing, name="add_listing"),
    path("listings/comment", views.add_comment, name="add_comment"),
    path("listings/bid", views.place_bid, name="place_bid"),
    path("listings/watch/<int:list_id>", views.watch_item, name="watch"),
    path("listings/unwatch/<int:list_id>", views.unwatch_item, name="unwatch"),
    path("listings/watchlist", views.watchlist, name="watchlist"),
    path("listings/categories", views.categories, name="categories"),
    path("listings/categories/<int:cat_id>", views.category_details, name="category_details"),
    path("listings/close/<int:list_id>", views.close_auction, name="close")

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("showCategory", views.showCategory, name="showCategory"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("addBid/<int:listing_id>", views.addBid, name="addBid"),
    path("endAuction/<int:listing_id>", views.endAuction, name="endAuction"),
    path("restoreAuction/<int:listing_id>", views.restoreAuction, name="restoreAuction"),
    path("watchlist", views.watchlist, name="watchlist")
]

from django.urls import path

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListings,name="create"),
    path('closedAuctions', views.showClosed, name='showClose'),
    path("displayCategory",views.displayCategory,name="displayCategory"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("updateWatchlist/<int:id>",views.updateWatchlist,name="updateWatchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment"),
    path("addBid/<int:id>",views.addBid,name="addBid"),
    path("closeAuction/<int:id>",views.closeAuction,name="closeAuction"),

]

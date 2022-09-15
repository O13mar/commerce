# from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import listForm

from .models import User, Category, Listings, Comment, Bid, Watchlist


def listing(request, id):
    listingData = Listings.objects.get(pk=id)
    allComments = Comment.objects.filter(listing=listingData.id).all()
    if not listingData.isactive:
        winner = Bid.objects.filter(list=listingData).last().user.username
    else:
        winner = None
    try:
        list = Watchlist.objects.filter(
            user=request.user,
            list=id
        )
    except:
        list = None

    onwatch = True if list else False
    owner = True if request.user == listingData.user else False
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "allComments": allComments,
        'onwatch': onwatch,
        'owner': owner,
        'winner':winner

    })


def closeAuction(request, id):
    listingData = Listings.objects.get(pk=id)
    listingData.isactive = False
    listingData.save()
    allComments = Comment.objects.filter(listing=listingData).all()

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "allComments": allComments,
        "update": True,
        "message": "Congratulation your auctions is closed"
    })


def addBid(request, id):
    newBid = request.POST['newBid']
    newBid = float(newBid)
    list = Listings.objects.get(id=id)

    if newBid > list.price:
        obj = Bid.objects.create(
            user=request.user,
            list=list,
            bid=newBid
        )
        obj.save()
        list.price = newBid
        list.save()
        return redirect("listing", list.id)
    else:
        context = {
            "listing": list,
            "updated": False,
            "allComments": Comment.objects.filter(listing=list.id).all()
        }
        return render(request, "auctions/listing.html", context)


def addcomment(request, id):
    currentUser = request.user
    listingData = Listings.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def watchlist(request):
    list = Watchlist.objects.filter(
        user=request.user
    ).all()
    return render(request, "auctions/watchlist.html",
                  {
                      "listing": list
                  })


def updateWatchlist(request, id):
    subList = Listings.objects.get(id=id)
    listing = Watchlist.objects.filter(user=request.user).all()
    try:
        list = Watchlist.objects.filter(
            user=request.user,
            list=subList
        )
    except:
        list = None

    if list:
        list.delete()

        allcategories = Category.objects.all()
        activelisting = Listings.objects.filter(isactive=True).all()
        return render(request, "auctions/index.html", context={
            "listing": activelisting,
            "categories": allcategories
        })
    else:
        obj = Watchlist.objects.create(
            user=request.user,
            list=subList
        )
        obj.save()
        return render(request, "auctions/watchlist.html", context={
            "listing": listing
        })


def index(request):
    allcategories = Category.objects.all()
    activelisting = Listings.objects.filter(isactive=True).all()
    return render(request, "auctions/index.html",
                  {"listing": activelisting,
                   "categories": allcategories, }
                  )


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        allcategories = Category.objects.all()
        activelisting = Listings.objects.filter(isactive=True, category=category)
        return render(request, "auctions/index.html",
                      {"listings": activelisting,
                       "categories": allcategories, }
                      )


def createListings(request):
    form = listForm()
    if request.method == 'POST':
        form = listForm(request.POST)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
    return render(request, "auctions/create.html", context={
        "form": form
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def showClosed(request):
    list = Listings.objects.filter(isactive=False).all()
    return render(request, "auctions/closedNav.html", context={
        "listing":list
    })


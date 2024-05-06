from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Category, Comments, Bid

class NewListingForm(forms.Form):
    title = forms.CharField(label='Listing Title')
    content = forms.CharField(label='Content', widget=forms.Textarea)
    cost = forms.IntegerField(label='Starting Bid')
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    image = forms.CharField(label='Image URL')

class NewBidForm(forms.Form):
    cost = forms.IntegerField(label="Enter Bid")

def index(request):
    liveListings = Listing.objects.filter(isLive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": liveListings,
        "categories": allCategories
    })

def showCategory(request):
    if request.method == "POST":
        allCategories = Category.objects.all()
        selectedCategory = request.POST["category"]
        category = Category.objects.get(categoryTitle=selectedCategory)
        categoryListings = Listing.objects.filter(isLive=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": categoryListings,
            "categories": allCategories
        })

def addBid(request, listing_id):
    if request.method == "POST":
        newBid = int(request.POST["addBid"])
        current_listing = Listing.objects.get(pk=listing_id)
        currentUser = request.user
        currentBid = int(current_listing.cost.bid)
        # somehow log or echo the result of currentBid
        print(currentBid)  # This will print the bid amount to the console
        if newBid > currentBid:
            # Make new bid db object and save
            winningBid = Bid(bid=newBid, user=currentUser)
            winningBid.save()

            # Update the cost field of the Listing object
            current_listing.cost = winningBid
            current_listing.save()

            return HttpResponseRedirect(reverse("listing",args=(listing_id, )))
        else:
            # newBid is smaller than currentBid, so display a message that the bid was not updated and needs to be higher
            messages.error(request, 'Your bid needs to be higher than the current bid.')
            return HttpResponseRedirect(reverse("listing",args=(listing_id,)))
            
    
def create(request):
    if request.method == "POST":
        
        # Get the form fields from submission
        title = request.POST["title"]
        content = request.POST["content"]
        cost = request.POST["cost"]
        category_id = request.POST["category"]
        image = request.POST["image"]

        # Get logged in user that made request
        currentUser = request.user

        # Make new bid db object and save
        newBid = Bid(bid=int(cost), user=currentUser)
        newBid.save()

        # Get the actual category id based off the string value
        category = Category.objects.get(id=category_id)
        new_listing = Listing(title=title, content=content, cost=newBid, category=category, image=image, author=currentUser )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    
    # Need to handle session and listing object
    else:
        return render(request, "auctions/create.html", {
            "form": NewListingForm() 
            })    

def listing(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    isInWatchlist = request.user in current_listing.watchlist.all()
    isWinning = request.user == current_listing.cost.user
    isOwner = request.user == current_listing.author
    isLive = current_listing.isLive
    print(isWinning)
    hasComments = Comments.objects.filter(listing=current_listing)
    return render(request, "auctions/listing.html", {
            "listing": current_listing,
            "isInWatchlist": isInWatchlist,
            "Comments": hasComments,
            "isOwner" : isOwner,
            "isLive" : isLive,
            "isWinning" : isWinning
        })

def endAuction(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    current_listing.isLive = False
    current_listing.save()
    return HttpResponseRedirect(reverse("listing",args=(listing_id, )))

def restoreAuction(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    current_listing.isLive = True
    current_listing.save()
    return HttpResponseRedirect(reverse("listing",args=(listing_id, )))

def addToWatchlist(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    current_listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(listing_id, )))

def removeFromWatchlist(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    current_listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(listing_id, )))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
            "listings": listings
        })

def addComment(request, listing_id):
    if request.method == "POST":
        current_listing = Listing.objects.get(pk=listing_id)
        currentUser = request.user
        comment = request.POST["addComment"]

        newComment = Comments(
            author=currentUser,
            listing=current_listing,
            message=comment
        )

        newComment.save()

        return HttpResponseRedirect(reverse("listing",args=(listing_id, )))



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


    


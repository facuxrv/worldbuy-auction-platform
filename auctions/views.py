from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

from .models import User


def index(request):
    AuctionListings_set = AuctionListings.objects.filter(auction_active=True)
    if not AuctionListings_set.exists():
        return render(request, "auctions/index.html", {
            "message": "No active listings available."
        })
    else: 
        return render(request, "auctions/index.html", {
            "AuctionListings": AuctionListings_set
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
            messages.error(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
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
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    # We retrieve the information from user input
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url", "")
        category = request.POST.get("category", "")
        owner = request.user
        current_bid = None
        # If the starting bid is not provided, we set it to 0.00
        if starting_bid is None or starting_bid == "":
            starting_bid = 0.00
        # Create the auction listing
        AuctionListings.objects.create(
            title=title,
            description=description,
            current_bid=current_bid,
            image_url=image_url,
            category=category,
            owner=owner,
            starting_bid=starting_bid
        )
        messages.success(request, f"Your auction listing '{title}' has been created successfully!")
        return HttpResponseRedirect(reverse("index"))
    # If the request method is GET, we render the create listing form
    else:
        return render(request, "auctions/create_listing.html")
    
def listing(request, listing_id):
    # If the request method is GET, we retrieve the listing as long it exists
    if request.method == "GET":
        try:
            listing = AuctionListings.objects.get(id=listing_id)
        except AuctionListings.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "message": "Listing not found."
            })
        # If the listing exists, we render it
        return render(request, "auctions/listing.html", {
            "listing": listing
    })
    # If the request method is POST, we handle the actions on the listing
    elif request.method == "POST":
        # Check if the listing exists
        try:
            listing = AuctionListings.objects.get(id=listing_id)
        except AuctionListings.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "message": "Listing not found."
            })

        # Handle listing deletion
        if request.POST.get("delete_listing"):
            listing_title = listing.title
            listing.delete()
            messages.success(request, f"Listing '{listing_title}' has been deleted successfully.")
            return HttpResponseRedirect(reverse("index"))
        
        # Handle bidding
        elif request.POST.get("bid_amount"):
            bid_amount = request.POST.get("bid_amount")
            # Determine the minimum bid required
            minimum_bid = listing.starting_bid
            if listing.current_bid is not None:
                minimum_bid = listing.current_bid.amount
            
            if bid_amount is not None and float(bid_amount) > minimum_bid:
                new_bid = Bid.objects.create(
                    user=request.user,
                    listing=listing,
                    amount=float(bid_amount)
                )
                listing.current_bid = new_bid
                listing.save()
                messages.success(request, f"Your bid of ${bid_amount} has been placed successfully!")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                messages.error(request, f"Bid must be greater than ${minimum_bid}.")
                return render(request, "auctions/listing.html", {
                    "listing": listing
                })
            
        # Handle comments
        elif request.POST.get("commenttext"):
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to comment.")
                return render(request, "auctions/listing.html", {
                    "listing": listing
                })
            comment_content = request.POST.get("commenttext")
            if comment_content is not None:
                Comment.objects.create(
                    user=request.user,
                    listing=listing,
                    content=comment_content
                )
                messages.success(request, "Your comment has been added successfully!")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            elif comment_content == "":
                messages.warning(request, "Comment cannot be empty.")
                return render(request, "auctions/listing.html", {
                    "listing": listing
                })
            
        # Handle closing the auction

        elif request.POST.get("close_listing"):
            if listing.current_bid and listing.current_bid.user != request.user:
                listing.auction_active = False
                listing.save()
                messages.success(request, f"Auction for '{listing.title}' has been closed successfully.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                messages.error(request, "You cannot close this auction.")
                return render(request, "auctions/listing.html", {
                    "listing": listing
                })
            
        # Handle adding to watchlist

        elif request.POST.get("add_to_watchlist"):
            Watchlist.objects.create(
                user=request.user,
                listing=listing
            )
            messages.success(request, f"'{listing.title}' has been added to your watchlist!")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            messages.warning(request, "Something went wrong. Please try again.")
            return render(request, "auctions/listing.html", {
                "listing": listing
            })

# Handle the watchlist view, showing the user's watchlist
def watchlist(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Fetch the user's watchlist listings
    watchlist_listings = AuctionListings.objects.filter(
        watchlist__user=request.user
    )
    # If no listings are found, we should return a message
    if not watchlist_listings.exists():
        return render(request, "auctions/watchlist.html", {
            "message": "No listings in your watchlist."
        })
    # Render the watchlist
    return render(request, "auctions/watchlist.html", {
        "WatchList": watchlist_listings
    })

# We handle the category view, giving the user the auctions in a given category
def category(request, category_name):
    # Check if the category name is provided
    if category_name == "" or not category_name:
        return render(request, "auctions/choosecategories.html")
    # Fetch listings for the given category
    listings = AuctionListings.objects.filter(category=category_name)
    # If no listings are found, we return a message
    if not listings.exists():
        return render(request, "auctions/choosecategories.html", {
            "message": "No listings found in this category."
        })
    # Render the listings for the category
    return render(request, "auctions/categories.html", {
        "listings": listings,
        "category_name": category_name
    })

# This view allows users to choose a category from the available auction listings
def choose_categories(request):
    # Fetch distinct categories from the AuctionListings model
    categories = AuctionListings.objects.values_list('category', flat=True).distinct()
    # If no categories are found, we return a message
    if not categories:
        return render(request, "auctions/choosecategories.html", {
            "message": "No categories available."
        })
    # Render the categories for the user to choose from
    return render(request, "auctions/choosecategories.html", {
        "categories": categories
    })
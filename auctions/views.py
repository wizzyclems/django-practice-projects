from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Listing, User,Bid,Comment
from .forms import AddListingForm, BidForm, CommentForm


def index(request):
    listing = Listing.objects.all()

    return render(request, "auctions/index.html",{
        "listing": listing
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


def addListing(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        listingForm = AddListingForm(request.POST, request.FILES)

        if listingForm.is_valid():
            title = listingForm.cleaned_data["title"]
            description = listingForm.cleaned_data["description"]
            startBid = listingForm.cleaned_data["startBid"]
            categories = listingForm.cleaned_data["category"]
            #categories = [c for c in categories]
            #print(categories)
            photo = listingForm.cleaned_data["photo"]

            #TODO
            #1. adjust the dimensions of the uploaded image
            #2. change the name of the uploaded image to ensure uniqueness
            print(photo.image)
            print(photo.image.width)
            print(photo.image.height)
            print(photo.image.format)
            
            #print(f"{title}:{description}:{startBid}:{categories}:{photo}") 
            user = request.user
            
            #TODO - save the form
            
            try:
                
                #listing = Listing(args={"title":title,"description":description,
                #"startBid":startBid,"photo":None,"user":user,"categories":categories})
                
                listing = Listing()
                listing.title = title
                listing.description = description
                listing.startBid = startBid
                listing.photo = photo
                listing.user = user

                listing.save()

                listing.categories.set(categories)
                
            except IntegrityError:
                return render(request, "auctions/add_listing.html", {
                    "message": "Similar Listing already exist.",
                    "addListingForm": listingForm
                })
            except Exception:
                return render(request, "auctions/add_listing.html", {
                    "message": "An error occurred while adding listing. Ensure your form is correctly filled.",
                    "addListingForm": listingForm
                })

        else:
            print("*** The form is not valid")
            
            return render(request, "auctions/add_listing.html", {
                "addListingForm": listingForm
            })
        
    else:
        print("*** user will be redirected the the main listing page.")
        listingForm = AddListingForm()
        return render(request, "auctions/add_listing.html", {
            "addListingForm": listingForm
        })
        
    
    return HttpResponseRedirect(reverse("index"))



def listing_detail(request,list_id):
    print(f"Search for a listing details with id {list_id}")

    try:
        listing = Listing.objects.get(id=list_id)
    except Listing.DoesNotExist:
        listing = None

    commentForm = CommentForm()
    bidForm = BidForm()

    if listing :
        commentForm.initial['list_id'] = listing.id
        bidForm.initial['list_id'] = listing.id

    print(f"The search listing is : {listing} ")
    return render(request, "auctions/listing_view.html", {
        "listing": listing,
        "bidForm": bidForm,
        "commentForm": commentForm
    })


def place_bid(request):

    if request.method == 'POST':
        message = ""
        bidForm = BidForm(request.POST)
        commentForm = CommentForm()

        list_id = request.POST["list_id"]
        listing = Listing.objects.get(id=list_id)

        if bidForm.is_valid():
            print(f"***The bid form is valid.")
            bid = request.POST["bid"]
            
            user = request.user
            bid = Bid(bid=bid,listing=listing,user=user)

            try:
                bid.save()
                print(f"Bid: <{bid}> has been saved successfully")
                message = "Your Bid has been successfully saved."
                bidForm = BidForm()
            except Exception:
                print(f"An error occurred while saving your bid. Kindly try again. -> {bid}")
                message = "An error occurred while saving your bid. Kindly try again."
            finally:
                bidForm.initial['list_id'] = listing.id # I don't think we need this line though since the id may still be in the returned request
        else:
            print(f"**************The bid form is not valid")
    
        commentForm.initial['list_id'] = listing.id

        return render(request, "auctions/listing_view.html",{
            "listing": listing,
            "bidForm": bidForm,
            "commentForm": commentForm,
            "message": message
        })
    else:
        return HttpResponseRedirect(reverse("index"))


def add_comment(request):
    
    if request.method == 'POST':
        message = ""
        commentForm = CommentForm(request.POST)
        bidForm = BidForm()

        list_id = request.POST["list_id"]
        listing = Listing.objects.get(id=list_id)

        if commentForm.is_valid():
            print(f"***The comment form is valid.")
            text = request.POST["text"]
            
            user = request.user
            comment = Comment(text=text,listing=listing,user=user)

            try:
                comment.save()
                print(f"Comment: <{comment}> has been saved successfully")
                message = "Your Comment has been successfully saved."
                commentForm = CommentForm()
            except Exception:
                print(f"An error occurred while saving your comment. Kindly try again. -> {comment}")
                message = "An error occurred while saving your comment. Kindly try again."
            finally:
                commentForm.initial['list_id'] = listing.id # I don't think we need this line though since the id may still be in the returned request
        else:
            print(f"**************The comment form is not valid")
    
        bidForm.initial['list_id'] = listing.id

        return render(request, "auctions/listing_view.html",{
            "listing": listing,
            "bidForm": bidForm,
            "commentForm": commentForm,
            "message": message
        })
    else:
        return HttpResponseRedirect(reverse("index"))

































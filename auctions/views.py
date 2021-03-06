from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import AddBidForm
from .forms import AddCommentForm
from .forms import AddListingForm
from .models import AuctionListing
from .models import Bid
from .models import Comments
from .models import User
from .models import Wishlist
from .models import Category
from .models import Winner

def close_bid(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    listing.sold = True
    listing.save()

    #TODO save user id and product id in the winner model
    try:
        last_bid = Bid.objects.filter(product=listing).latest('value')
        winner = Winner(user= last_bid.author, product= listing)
        winner.save()
    except:
        pass
    return render(request, "auctions/index.html")


def category_detail(request, category_id):
    category=Category.objects.get(id=category_id)
    list_of_items = AuctionListing.objects.filter(category=category).all()
    print(list(list_of_items))
    context = {'category': category, 'list_of_items': list_of_items}
    return render(request,"auctions/category_detail.html", context)

def category_list(request):
    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return render(request, 'auctions/category_list.html', context)


def wishlist_add(request, listing_id):
    '''
    get user and product id from Template
    get queryset from wishlist model filtered by user and product
    if queryset does not exist
        add entry
    else
        remove entry
    '''

    user = request.user
    filtered_user = Wishlist.objects.filter(user=user, product=listing_id)
    if not filtered_user:
        print(f"{user} , does not have {listing_id} in wishlist")
        product = AuctionListing.objects.get(pk=listing_id)
        entry = Wishlist(user=user, product=product)
        entry.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        print(f"{user} has {listing_id}")
        Wishlist.objects.filter(user=user, product=listing_id).delete()
        return HttpResponseRedirect(reverse('index'))
    #return user related wihslist product. ( I think this should be sent fomr the index view.


def wishlist(request):
    user = request.user
    wishlist_objects = Wishlist.objects.filter(user=user)
    print(wishlist_objects)
    context = {'wishlist_objects': wishlist_objects}
    return render(request, 'auctions/wishlist.html', context)


def index(request):
    user = request.user
    auction_listing_objects = AuctionListing.objects.all()
    try:
        won_products = Winner.objects.filter(user=user).all()
    except:
        pass

    context = {"products": auction_listing_objects}
    if won_products:
        context.update({"won_products": won_products})
    return render(request, "auctions/index.html", context)


def listing_detail(request, listing_id): #TODO: ADD CLOSING BID LOGIC HERE
    # print(listing_id)
    listing = AuctionListing.objects.get(id=listing_id)
    try:
        last_bid = Bid.objects.filter(product=listing).latest('value')
    except:
        last_bid = 0
    print(listing)
    if listing.sold == True:
#       last_bid = Bid.objects.filter(product=listing).latest('value')
        print(last_bid)
        if request.user == last_bid.author:
            message = "Congratulation, you won the bid!"
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "message": message,

            })
        
        #higher_bid = Bid.objects.filter(product=product).order_by('-value').values_list('value', flat=True)
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "last_bid": last_bid,
    })


def listing_add(request):
    form = AddListingForm()
    if request.method == "POST":
        print(f"the user is {request.user.id}")
        form = AddListingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            print(f"the form  is {obj}")
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, "auctions/listing_add.html", context)


def comment_add(request, listing_id):
    form = AddCommentForm()
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = AuctionListing.objects.get(pk=listing_id)
            comment.comment = form.cleaned_data['comment']
            comment.author = request.user
            form.save()
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'auctions/comment_add.html', context)


def bid_add(request, listing_id):  # see important lesson at the end.
    form = AddBidForm()

    if request.method == "POST":
        form = AddBidForm(request.POST or None)
        if form.is_valid():
            author = request.user
            product = AuctionListing.objects.get(id=listing_id)
            initial_value = product.initial_price
            bid = form.save(commit=False)
            bid.author = author
            bid.product = product
            bid_value = int(form.cleaned_data['value'])
            # check if author is the same as the bidder

            if author.id == product.user.id:
                # print("same author")
                messages.error(request, "your bid is not going to be registered: same user")
                return HttpResponseRedirect(reverse('bid_add', args=(listing_id,)))

            # check if bid is lower than initial value.
            if bid_value < initial_value:
                # print(f"price too low to start{bid_value} <= {initial_value}")
                messages.error(request, "You are bidding below the initial price")
                return HttpResponseRedirect(reverse('bid_add', args=(listing_id,)))

            # check if bid is lower than higher one
            higher_bid = Bid.objects.filter(product=product).order_by('-value').values_list('value', flat=True)
            if higher_bid:
                if int(bid_value) <= higher_bid[0]:
                    print(f"price too low {bid_value} <= {higher_bid[0]}")
                    messages.error(request, "You are bidding below the highest bid")
                    return HttpResponseRedirect(reverse('bid_add', args=(listing_id,)))

            bid.save()
            messages.success(request,"Bid successfully added, good luck!")
            return HttpResponseRedirect(reverse('bid_add', args=(listing_id,)))
    context = {'form': form}
    return render(request, 'auctions/bid_add.html', context)


'''
            product = AuctionListing.objects.filter(id=listing_id).values("description")

            # this output the queryset
            product2 = AuctionListing.objects.filter(id=listing_id).values_list('description')

            # this output a tuple
            product3 = AuctionListing.objects.values_list("description").get(id=listing_id)

            # this is what i want!
            product4 = AuctionListing.objects.get(id=listing_id)
            #print(f"{product[0]['description']} - {product2} - {product3} - {product4.description}")
'''


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

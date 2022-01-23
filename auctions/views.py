from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from.forms import AddListingForm, AddCommentForm
from .models import User, AuctionListing, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "products": AuctionListing.objects.all()
    } )


def listing_detail(request, listing_id):
    print(listing_id)
    listing = AuctionListing.objects.get(id=listing_id)
    print(listing)
    return render(request, "auctions/listing_detail.html", {
        "listing": listing
    })


def listing_add(request):
    form = AddListingForm()

    if request.method == "POST":
        form = AddListingForm(request.POST)
        if form.is_valid():
            form.save()
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


def bid_add(request, product_id):
    pass


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

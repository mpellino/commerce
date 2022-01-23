from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionListing, Comments, Bid

admin.site.register(User, UserAdmin)

admin.site.register(AuctionListing)

admin.site.register(Comments)

admin.site.register(Bid)

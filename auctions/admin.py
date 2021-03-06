from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import AuctionListing
from .models import Bid
from .models import Comments
from .models import User
from .models import Wishlist
from .models import Category
from .models import Winner

admin.site.register(User, UserAdmin)

admin.site.register(AuctionListing)

admin.site.register(Comments)

admin.site.register(Bid)

admin.site.register(Wishlist)

admin.site.register(Category)

admin.site.register(Winner)
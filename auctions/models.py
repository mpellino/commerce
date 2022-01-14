from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    product = models.CharField(max_length=255)
    description = models.TextField(default="none")
    category = models.CharField(max_length=255)
    initial_price = models.PositiveIntegerField(default=0)
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product
    
    def get_absolute_url(self):
        reverse('auction_list')


class Bid(models.Model):
    pass


class Comments(models.Model):
    pass


class AuctionWinner(models.Model):
    pass

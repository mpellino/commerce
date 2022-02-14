from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
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
        return f"{self.product}"
    
    def get_absolute_url(self):
        reverse('auction_list')


class Comments(models.Model):
    product = models.ForeignKey(AuctionListing, related_name="comments", on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=140 , default=None)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        default=None,
        related_name="author"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('index')


class Bid(models.Model):
    value = models.PositiveIntegerField(default=None)
    product = models.ForeignKey(AuctionListing, related_name="bid", on_delete=models.CASCADE, default=None)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        default=None,
        related_name="bid"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return str(self.value)

    def get_absolute_url(self):
        return reverse('index')


class Wishlist(models.Model):
    product = models.ForeignKey(AuctionListing, related_name="wishlist_product",
                                on_delete= models.CASCADE,
                                null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} on wishlist for {self.user}"

    def get_absolute_url(self):
        reverse('auction_list')

class AuctionWinner(models.Model):
    pass

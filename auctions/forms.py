from django.forms import ModelForm
from .models import AuctionListing


class AddListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
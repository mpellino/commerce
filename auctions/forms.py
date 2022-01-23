from django.forms import ModelForm
from .models import AuctionListing, Comments, Bid


class AddListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
        
        
class AddCommentForm(ModelForm):
    class Meta:
        model = Comments
        exclude = ('author', 'product')


class AddBidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ('author', 'product')
            
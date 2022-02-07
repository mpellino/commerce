from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
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
    value = forms.DecimalField()

    class Meta:
        model = Bid
        fields = '__all__'

    def clean_value(self, *args, **kwargs):
        value = self.cleaned_data['value']
        if not value > 0:
            raise forms.ValidationError(_('Invalid bid'))
        
        return value
            
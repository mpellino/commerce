from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _

from .models import AuctionListing
from .models import Bid
from .models import Category
from .models import Comments

choice = Category.objects.all().values_list('name', 'name')
choice_list = []

for item in choice:
    choice_list.append(item)

class AddListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
        exclude = ('sold', 'user',)
        widgets = {
            'category': forms.Select(choices = choice_list, attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'cols': 30, 'rows': 5}),
        }
        labels = {
            'description': _('Description'),
        }
        

class AddCommentForm(ModelForm):
    class Meta:
        model = Comments
        exclude = ('author', 'product')


class AddBidForm(ModelForm):
    value = forms.DecimalField()

    class Meta:
        model = Bid
        fields = ['value']

    def clean_value(self, *args, **kwargs):
        value = self.cleaned_data['value']
        if not value > 0:
            raise forms.ValidationError(_('Invalid bid'))
        
        return value
            
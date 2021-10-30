from django import forms

from auctions.models import Category

class AddListingForm(forms.Form):
    title = forms.CharField(min_length=3, widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':10,'rows':3}))
    startBid = forms.CharField(widget=forms.NumberInput())
    categories = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=categories)
    photo = forms.ImageField()
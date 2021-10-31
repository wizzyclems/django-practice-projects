from django import forms

from auctions.models import Category

class AddListingForm(forms.Form):
    title = forms.CharField(min_length=3, widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':10,'rows':3}))
    startBid = forms.CharField(widget=forms.NumberInput())
    categories = Category.objects.all()
    category = forms.ModelMultipleChoiceField(queryset=categories)
    photo = forms.ImageField()


class BidForm(forms.Form):
    bid = forms.CharField(widget=forms.NumberInput())
    list_id = forms.CharField(widget=forms.HiddenInput())

    def clean_bid(self):
        bid = self.cleaned_data.get("bid")
        list_id = self.cleaned_data.get("list_id")

        print(f"The list item for bid is {list_id}")

        return bid



class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':10,'rows':2}))

    list_id = forms.CharField(widget = forms.HiddenInput(), required = False)

    def clean_text(self):
        text = self.cleaned_data.get("text")
        list_id = self.cleaned_data.get("list_id")

        print(f"The list item for bid is {list_id}")

        return text

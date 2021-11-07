from django import forms

from auctions.models import Category,Bid, Listing


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

    def clean(self):
        #cleaned_data = super().clean()
        bid = self.cleaned_data.get('bid')
        list_id = self.cleaned_data.get('list_id')
        print(f"**********clean data {self.cleaned_data}")
        print(f"*****The bid is {bid}")
        print(f"******The list item for bid is {list_id}")

        try:
            list = Listing.objects.get(id=list_id)
        except Listing.DoesNotExist:
            list = None

        highest_bid = Bid.objects.filter(listing__id=list_id,highest=True)
        
        if highest_bid :
            print(f"highest bid : {highest_bid} is valid")
            if not int(bid) > highest_bid.first().bid:
                msg = 'Your bid must be higher than the current price.'
                raise forms.ValidationError(msg)
        else:
            print(f"No highest bid")
            if not bid or not list:
                msg = 'Your bid cannot not be empty and must be higher than the current price.'
                raise forms.ValidationError(msg)

            if not int(bid) >= list.startBid:
                msg = 'Your bid must be higher than the current price.'
                raise forms.ValidationError(msg)
        

        return self.cleaned_data



class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':10,'rows':2}))

    list_id = forms.CharField(widget = forms.HiddenInput(), required = False)

    def clean_text(self):
        text = self.cleaned_data.get("text")
        list_id = self.cleaned_data.get("list_id")

        print(f"The list item for bid is {list_id}")

        return text

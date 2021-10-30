from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, related
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.lookups import StartsWith


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    startBid = models.BigIntegerField()
    photo = models.ImageField(upload_to='static/auction_photos')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    categories = models.ManyToManyField(Category, related_name='listings')

    

    def __str__(self) -> str:
        #cat = [ c.title for c in self.categories.all() ]
        #c = ",".join(cat)
        #return f"{self.title}[{ c }] -> Starting Bid: ${self.startBid}"
        return f"{self.title} -> Starting Bid: ${self.startBid}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
    bid = models.BigIntegerField()

    def __str__(self) -> str:
        return f"{self.listing.title}({self.user}) : ${self.bid}"


    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='list_item')
    text = models.CharField(max_length=255)


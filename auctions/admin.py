from django.contrib import admin

from auctions.models import Category,User,Comment, Bid, Listing


class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","first_name","last_name", "email" )


class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories", )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing,ListingAdmin)
admin.site.register(Category)
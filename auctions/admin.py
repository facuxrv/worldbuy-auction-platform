from django.contrib import admin
from .models import User, AuctionListings, Bid, Comment

admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Bid)
admin.site.register(Comment)

# Register your models here.

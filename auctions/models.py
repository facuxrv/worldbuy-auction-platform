from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_bid_listing')
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    auction_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.amount}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}: {self.content[:20]}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"
from django.contrib.auth.models import AbstractUser
from django.db import models

#Models: Your application should have at least three models in addition to the User model:
# one for auction listings, one for bids, and one for comments made on auction listings. 
class User(AbstractUser):
    pass

class Category(models.Model):
    categoryTitle = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryTitle
 
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidUser")

    def __str__(self):
        return f" {self.bid}"
    
class Listing(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=20)
    image = models.URLField()
    cost = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="cost")
    isLive = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return f" {self.title} {self.content} {self.category} {self.image} {self.cost}"
    
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentAuthor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="commentListing")
    message = models.CharField(max_length=80)

    def __str__(self):
        return f" {self.author} {self.listing} {self.message}"
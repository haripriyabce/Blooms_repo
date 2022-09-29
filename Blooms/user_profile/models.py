from django.db import models
from product.models import Product
from admin_p.models import Users
# Create your models here.
class Wishlist(models.Model):   
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.id)

class WishlistItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.product_name
        
class Review(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    title  = models.TextField(max_length=100, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)

    
    def __str__(self):
        return str(self.id)

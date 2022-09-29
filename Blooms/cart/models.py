from django.db import models
from product.models import Product
from admin_p.models import Users,Shipping_Address

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cart(models.Model):
    carts_id = models.CharField(max_length=150,blank=True)
   
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True )
    addressid= models.ForeignKey(Shipping_Address,on_delete=models.SET_NULL,blank=True, null=True)
   
    final_price =models.FloatField( blank=True, null=True , default = 0)
    date_carted = models.DateField(null=True)
    date_delivery = models.DateField(null=True)
    coupon_applied =models.CharField(max_length=30,blank=True,null= True, default=0)
    final_offer_price =models.FloatField( blank=True, null=True , default = 0)
   
  
    

    def __str__(self):        
        return f'{self.carts_id}'
    
class cartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    price = models.FloatField(null=True)
    quantity=models.IntegerField(default=0)
   
       
    date_carted = models.DateField(null=True)
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
  
    is_active = models.BooleanField(default=True)
    
    

    @property
    def get_total(self):
        total=self.price*self.quantity
        return total
    
    # @property
    # def get_cart_total(self):
    #     cartitems=self.cartitem_set.all()
    #     total=sum([item.get_total for item in cartitems])
    #     return total
    # @property
    # def get_cart_items(self):
    #     cartitems=self.cartitem_set.all()
    #     total=sum([item.quantity for item in cartitems])
    #     return total
    
    # def __str__(self):
    #     return f'{self.cart}'
    
class Coupon(models.Model):
        
    coupon_code = models.CharField(max_length=30,unique=True)
    valid_from = models.DateTimeField( null = True)
    valid_to = models.DateTimeField( null = True )
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    min_purchase=models.IntegerField(null = True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_code
    class  Meta:
        ordering = ['-valid_to',]



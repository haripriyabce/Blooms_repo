from django.db import models
from product.models import Product
from admin_p.models import Users,Shipping_Address
class Payment(models.Model):
    payment_mode = [ 

        ('COD','COD'),
        ('PAYPAL','PAYPAL'),
        ('RAZOR_PAY','RAZORPAY')
    ]
    STATUS =(
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Users,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100,choices=payment_mode)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Order(models.Model):    
    STATUS = (        
        ('Order Placed','Order Placed'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'), 
        ('Cancelled','Cancelled'),      
    )
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)    
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50, null=True)
    town= models.CharField(max_length=50 ,blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10 ,  blank=True, null=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField(blank=True, null=True)
    address= models.ForeignKey(Shipping_Address,on_delete=models.SET_NULL,related_name='address' ,blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS, default='Order Placed')
    coupon_applied =models.CharField(max_length=30,blank=True,null= True, default=0)
    # coupon_applied = models.BooleanField( default= False )
    # coupon = models.CharField( blank=True , max_length=30)

    guest = models.CharField(max_length=100,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    
    class Meta:
        ordering = ['-created_at','-updated_at']

class Order_Product(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    discount= models.IntegerField(null=True) 
    discount_price=models.FloatField(null=True)

    def sub_total(self):
        return self.product_price * self.quantity    

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering= ('-created_at','-updated_at')


   
class Product_off(models.Model):    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)     
    discount = models.IntegerField()
    def __str__(self):
        return str(self.product)
    


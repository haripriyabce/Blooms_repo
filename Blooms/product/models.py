from django.db import models
from category.models import *
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Variation(models.Model):
    variation_category = models.CharField(max_length=100)    
    created_date = models.DateTimeField(auto_now =True,null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.variation_category 
class Variation_value(models.Model):
    variation_category = models.ForeignKey(Variation,on_delete=models.CASCADE)
    variation_value=models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now =True,null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.variation_value 
    
class Product(models.Model):    
    product_name = models.CharField(max_length=200, unique=True)
    slug         = AutoSlugField(populate_from=['product_name'] ,unique=True)
    description  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField()
    offer_price = models.IntegerField(null=True, blank=True)
    offer_perc =  models.IntegerField(null=True, blank=True, default= 0)
   
    image1       = models.ImageField(upload_to = 'photos/products')
    image2       = models.ImageField(upload_to = 'photos/products',blank=True)
    image3       = models.ImageField(upload_to = 'photos/products',blank=True)
    

    stock        = models.IntegerField()
    Is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add =True)
    modified_date = models.DateTimeField(auto_now=True)
    product_offer = models.IntegerField(null=True, blank=True ,default= 0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Is_offer_active = models.BooleanField(default=True)
       
    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])
    
    
    def  __str__(self):
        return self.product_name
    
class Product_cate(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description  = models.TextField(max_length=500, blank=True)
    catid     = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory     = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    status= models.BooleanField(default=True)    
    
class Stock(models.Model):    
    product     = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productvariantstock')
    Variation = models.ForeignKey(Variation_value,on_delete=models.CASCADE,null=True,related_name='variantstock')
    stock        = models.IntegerField()
    price        = models.FloatField(null = True )
    def  __str__(self):
        return str(self.stock)
       
class Offer(models.Model):
    offer_name = models.CharField(max_length=50, unique = True )
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length =255, blank=True)
    offer_image = models.ImageField(upload_to = 'photos/offers/',blank=True)
    status = models.CharField(max_length=10,default=False )
    valid_from = models.DateTimeField( null = True)
    valid_to = models.DateTimeField( null = True )
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    
    is_active = models.BooleanField(default=True)
       

    def __str__(self):
        return self.offer_name
    

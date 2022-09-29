from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True )
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length =255, blank=True)
    category_image = models.ImageField(upload_to = 'photos/categories/',blank=True)
    status = models.CharField(max_length=10,default=False )
     
    class Meta:
        verbose_name = 'category'
        verbose_name_plural =  'categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])


    def __str__(self):
        return self.category_name
class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=50, unique = True )
    category     = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length =255, blank=True)
    status = models.CharField(max_length=10,default=False ) 
   
    def get_url(self):
        return reverse('products_by_subcategory',args=[self.slug])


    def __str__(self):
        return self.subcategory_name



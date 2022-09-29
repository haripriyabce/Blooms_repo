from django.db import models

# Create your models here.
class Content(models.Model):
    name = models.TextField(max_length =50, blank=True)
    image =models.ImageField( upload_to='photos/banner', height_field=None, width_field=None, max_length=None,blank=True)
    description = models.TextField(max_length =255, blank=True)
    is_selected = models.BooleanField(default=False)
    status = models.CharField(max_length=10,default='Active' )
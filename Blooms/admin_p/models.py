from datetime import date
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
#from order.models import Order
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name,username, email, password = None):
        if not email:
            raise ValueError("user must have an email address")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
           
        )
        user.is_active = True
        user.set_password(password)
        user.save(using= self._db)
        return user   
    
    def create_superuser(self, first_name,last_name, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name =last_name,
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    first_name =  models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    username =  models.CharField(max_length=100 , unique = True)
    email = models.EmailField(max_length=100 , unique=True)
    Phone_number = models.CharField(max_length=25,null = True, blank=True)
    password= models.CharField(max_length=250,blank=True, null=True)


    #required

    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth=models.DateTimeField(null=True)
    gender=models.CharField(max_length=25,blank=True, null=True)
    location=models.CharField(max_length=25,blank=True, null=True)
    alt_Phone_number = models.CharField(max_length=25,null = True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin =  models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_superadmin =  models.BooleanField(default=False)


    referel_code = models.CharField(max_length=50 , null=True , blank = True)
    referel_activated = models.BooleanField(default=False ,null = True )
   
     
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = MyAccountManager()

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

 
class Shipping_Address(models.Model):
    user = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
   
    #orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50, null=True)
    town= models.CharField(max_length=50 ,blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10 ,  blank=True, null=True)
    is_active =  models.BooleanField(default=True)
    is_default =  models.BooleanField(default=False) 
    date_ordered = models.DateTimeField(auto_now=True, null=True)
    

    def __str__(self):
        return str(self.id)
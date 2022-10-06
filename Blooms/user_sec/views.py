#from twilio.rest import Client
from ast import Try
import random
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect, render
from django.contrib import messages
from admin_p.models import Users
from product.models import Product,Product_cate,Stock
from content.models import Content
from order.models import Product_off
from category.models import Category,Subcategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages,auth
# Create your views here.
logo_light= Content.objects.get(name='logo_light')
def index1(request):
    z=False
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
        if 'username' in request.session:            
            print(request.session['user_id'])   
            z=True    
    products= Product.objects.all()[2:5]
    logo_light= Content.objects.get(name='logo_light')
    slider= Content.objects.filter(name='slider')    
    sec_banner1= Content.objects.get(name='sec_banner1') 
    sec_banner2= Content.objects.get(name='sec_banner2')    
    products1= Product.objects.all()[5:8]   
    print("z",z) 
    context = {
        'logo_light':logo_light,
        'slider':slider,
        'sec_banner1':sec_banner1,
        'sec_banner2':sec_banner2,
        'products1': products1,
        'products':products,
        'z':z,
        }       
    return render(request,'User/index.html',context)      
def login(request):    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']        
        if Users.objects.filter(username=email, password=password).exists():
            user = Users.objects.get(username=email, password=password)            
            if user is not None:
                auth.login(request,user)                    
                global otp
                otp = str(random.randint(1000,9999))
                print(otp) 
                
                # account_sid = "ACfb89df3b244d24d509cfeb86bad42469"
                # auth_token = "b0269ac8f0e13f4633f45b502e0a2fa0"
                # client = Client(account_sid, auth_token)

                # message = client.messages.create(
                #                             body='Hello there! Your Login OTP is' +otp,
                #                             from_='+18646592396',
                #                             to="+91"+user.Phone_number
                #                         )

                # print(message.sid)       
                messages.success(request,'OTP has been sent to '+user.Phone_number+' & enter OTP') 
                user_name = user
                print(user_name)
                context = { 
                           'logo_light':logo_light,
                           'user_name':user_name
                    }      
                return render(request,'User/login_otp.html',context)            
            #return redirect(login_otp)
        else :            
            messages.error(request,'invalid credentials')            
            return redirect(login)   
    context = { 
                           'logo_light':logo_light,
                    }             
    return render(request,'User/login.html',context)
def login_otp(request):    
    if request.method=='POST': 
        otpvalue = request.POST['otp']
        user_name = request.POST['usern']
        if len(otpvalue)>0:
            if otpvalue == otp:
                print(user_name)
                user = Users.objects.get(id=user_name)           
                #auth.login(request,user)
                request.session.flush()
                request.session['username'] = user_name
                request.session['user_id'] = user.id
                messages.success(request,'You are logged in')
                return redirect(index1)
            else:   
                messages.error(request,'Invalid OTP')
                return redirect(login_otp)
        else:
            messages.error(request,'Invalid OTP')
            return redirect(login_otp)
    # else:
    #     messages.error(request,'Invalid Phone number')
    #     return redirect(login)
    context = { 
                           'logo_light':logo_light,
                    }   
    return render(request,'User/login_otp.html',context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def register(request):
    if 'username' in request.session:
        return render(request,'home.html')        
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']   
        phone_number = request.POST['Phone_number']     
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']        
        if first_name=='' or last_name=='' or password1==''or phone_number=='':
            messages.info(request,'Please fill valid entries') 
            return redirect(register) 
        else:            
            if password1==password2:
                if Users.objects.filter(email=email).exists():
                    messages.info(request,'Email Taken')
                    return redirect(register)
                elif Users.objects.filter(Phone_number=phone_number).exists():
                    messages.info(request,'Phone number already exist')
                    return redirect(register)
                else:  
                    user = Users.objects.create(first_name=first_name,last_name=last_name,email=email,username=email,password=password1)
                    user.save()
                    user_name = user
                    global otps                    
                    otps = str(random.randint(1000,9999))
                    print(otps)           
                    # account_sid = "ACfb89df3b244d24d509cfeb86bad42469"
                    # auth_token = "b0269ac8f0e13f4633f45b502e0a2fa0"
                    # client = Client(account_sid, auth_token)
                    # message = client.messages.create(
                    #                             body='Hello there! Your Registration OTP is' +otps,
                    #                             from_='+18646592396',
                    #                             to="+91"+phone_number
                    #                         )
                    # print(message.sid)                                                                
                    context = {
                        'logo_light':logo_light,
                        'phone_number': phone_number,
                        'user_name':user_name,
                        
                    }
                    return render (request, 'User/otp_verification.html',context) 
                                       
            else:
                messages.info(request,'password not matching..')    
                return redirect(register) 
              
    else:
        context = {
                        'logo_light':logo_light,
         }
        
        return render(request,'User/register.html',context)

def otp_verification(request,Phone_number):
    user_name = request.GET.get('name')    
    if request.method=='POST':              
        otp3 =  request.POST['first']+ request.POST['second']+request.POST['third']+request.POST['fourth']
        print(otp3)   
        if otp3 == otps :
            if Users.objects.filter( id = user_name).exists():                
                use = Users.objects.get(id = user_name)
                email = use.email
                first = use.first_name
                last = use.last_name           
                referel = last+first+email
                use.Phone_number = Phone_number
                use.referel_code = referel
                use.save()    
                      
                messages.success(request,"registred successfully")
                return redirect (login)
        else:
            if Users.objects.filter( id = user_name).exists():                
                user = Users.objects.filter(id = user_name)
                user.delete()
                messages.success(request,"register unsuccessfull")
                return redirect ('register')
            else :               
                messages.success(request,"register unsuccessfull")
                return redirect ('register')
    else:
        context={
        'logo_light':logo_light,
        }      
        return render (request, 'User/otp_verification.html',context)    
def products(request,cat=None,sub=None):
    z=False
    print("now i am on list page")
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
        if 'username' in request.session:            
            print(request.session['user_id'])   
            z=True  
    print("l2")
    if 'username' in request.session:                   
        print("list3")   
        z=True 
    #cat = request.GET.get('cat')
    print('cat',cat)
    #sub = request.GET.get('sub') 
    print('sub',sub)
    if sub != None:
        products = Product_cate.objects.select_related('product').filter(subcategory_id = sub).distinct('product_id')
    elif cat != None:        
        products = Product_cate.objects.select_related('product').filter(catid_id = cat).distinct('product_id')       
    else:
        products= Product_cate.objects.select_related('product').all().distinct('product_id')           
    # if request.method == 'POST':
    #     search = request.POST["product_search"] 
    #     products = Product.objects.filter(product_name__icontains = search)
    #     return render(request,'Admin/product_list.html',{'products': products })
    categories =Category.objects.all()
    subcategories=Subcategory.objects.all()         
    pro_off=Product_off.objects.all()
    print(pro_off)
    return render( request,'User/product_list.html',{'products':products,'z':z,'logo_light':logo_light,'subcategories':subcategories,'categories':categories,'pro_off':pro_off})

def logout(request):
    request.session.flush()    
    messages.success(request,'you are logged out !')   
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
        if 'username' in request.session:            
            print(request.session['user_id'])  
    return redirect (login)

def product_det(request,id):
    z=False
    print("now i am on det page")
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
        if 'username' in request.session:            
            print(request.session['user_id'])   
            z=True  
    print("de2")
    if 'username' in request.session:                   
        print("de3")   
        z=True   
    discount=0
    pro= Product.objects.get(id=id)  
    try:
        pro_off=Product_off.objects.get(product_id=id) 
        discount=pro_off.discount
    except Product_off.DoesNotExist:        
        pass
    obj=None    
    pro_cate = Product_cate.objects.filter(product_id=id)
    if pro_cate.exists():
        obj = pro_cate.first() 
    
    products= Product_cate.objects.select_related('product').filter(catid_id=obj.id).distinct('product_id')[:2]  
    pro_off=Product_off.objects.all()   
    return render( request,'User/product_details.html',{'pro': pro,'products':products,'z':z,'logo_light':logo_light,'dis':discount,'pro_off':pro_off})



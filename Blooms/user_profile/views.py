from ast import For
from django.shortcuts import render,redirect
from content.models import Content
from django.contrib import messages
from order.models import Order, Order_Product
from admin_p.models import Users,Shipping_Address
from .models import Wishlist,WishlistItem
from product.models import Product
from cart.views import checkt_add
from cart.models import Coupon
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
# Create your views here.
logo_light= Content.objects.get(name='logo_light')
def myaddresses(request):  
    uss = Users.objects.get(id=request.session['user_id'])  
    d_address= Shipping_Address.objects.get(user=uss,is_active=True,is_default=True)
    addresses= Shipping_Address.objects.filter(user=uss,is_active=True,is_default=False)
    return render( request,'Profile/my_address.html',{'d_address':d_address,'addresses':addresses,'z':True,'logo_light':logo_light,})
def up_address(request,id):
    print("ggggggggggggg",request.META.get('HTTP_REFERER'))
    if request.method == "POST":  
        first_name= request.POST['first_name']  
        last_name= request.POST['last_name']                  
        phone_number = request.POST['Phone_number']
        email = request.POST['email']
        town = request.POST['add2']
        house = request.POST['add1']            
        state = request.POST['state']
        zip = request.POST['zip']  
        #RadioDefault = request.POST['RadioDefault']  
        RadioDefault=None
        try:
                RadioDefault = request.POST["RadioDefault"]
        except KeyError:
            RadioDefault = "None"
        if phone_number=='' or email=='' or house=='' or state=='' or town==''or zip=='' or first_name=='':
            messages.info(request,'Please fill valid entries')            
            return redirect(up_address(id))
        else:
            ship = Shipping_Address.objects.get(id=id)            
            ship.first_name = first_name
            ship.last_name = last_name
            ship.phone_number = phone_number
            ship.email = email
            ship.town = town
            ship.house = house
            ship.state = state
            ship.zip = zip
            ship.save()
            if RadioDefault==True: 
                Shipping_Address.objects.filter(user=request.session['user_id']).update(is_default=False) 
                ship.is_default=True
            ship.save()
            next = request.POST.get('next', '/')
            return redirect(next)
            #return redirect(myaddresses)                      
    ship=Shipping_Address.objects.get(id=id)
    return render(request,'Profile/up_address.html',{'ship':ship,'z':True})  

def add_address(request):  
    if request.method == 'POST':
        first_name= request.POST['first_name']  
        phone_number = request.POST['Phone_number']
        email = request.POST['email']
        town = request.POST['add2']
        house = request.POST['add1']            
        state = request.POST['state']
        zip = request.POST['zip']  
        
        if phone_number=='' or email=='' or house=='' or state=='' or town==''or zip==''or first_name=='':
            messages.info(request,'Please fill valid entries') 
            return redirect(add_address) 
        else:   
            if Shipping_Address.objects.filter(first_name = first_name,phone_number = phone_number,email = email,town = town,house = house,state = state,zip = zip).exists():
                messages.info(request,'Shipping_Address Already exists')
                return redirect(add_address)            
            else:   
                uss = Users.objects.get(id=request.session['user_id'])  
                Shipping_Address.objects.filter(user=request.session['user_id']).update(is_default=False) 
                ship= Shipping_Address.objects.create(user=uss,first_name = first_name,phone_number = phone_number,email = email,town = town,house = house,state = state,zip = zip)
                ship.save()
                print('Shipping_Address created')
                return redirect(myaddresses)             
    else:
        return render(request,'Profile/up_address.html')  
     
def myorders(request):
    orders=Order.objects.select_related('address').select_related('payment').filter(user=request.session['user_id']).order_by('-id')
    
    return render( request,'Profile/my_orders.html',{'orders':orders,'logo_light':logo_light})
def myorders_de(request,id):
    order=Order.objects.select_related('address').select_related('payment').get(id=id)
    orderitems=Order_Product.objects.select_related('product').filter(order_id=id)       
    return render( request,'Profile/Order_details.html',{'order':order,'orderitems':orderitems,'logo_light':logo_light}) 

def invoice(request,id):
    order=Order.objects.select_related('address').select_related('payment').get(id=id)
    total = order.order_total
    order_product=Order_Product.objects.select_related('product').filter(order_id=id)      
    
        
    context ={'order':order,'order_product':order_product,'total':total,'logo_light':logo_light}
    return render(request,'Order/invoice.html',context) 
def track_order(request,id):
    order=Order.objects.select_related('address').select_related('payment').get(id=id)
    total = order.order_total
    order_product=Order_Product.objects.select_related('product').filter(order_id=id)      
    
        
    context ={'order':order,'order_product':order_product,'total':total,'logo_light':logo_light}
    return render(request,'Order/track_order.html',context) 
def review(request,id):
       
    context ={'id':id,'logo_light':logo_light}
    return render(request,'Profile/add_review.html',context) 
              
        
def export_invoice_pdf(request,id):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=Invoice' +'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'
    order=Order.objects.select_related('address').select_related('payment').get(id=id)
    total = order.order_total
    order_product=Order_Product.objects.select_related('product').filter(order_id=id)       
       
        
    context ={'order':order,'order_product':order_product,'total':total,'logo_light':logo_light}


    html_string = render_to_string('Order/pdf_output_invoice.html',context)

    html=HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output : 
        output.write(result)
        output.flush()


        #output=open(output.name,'rb')
        output.seek(0)

        response.write(output.read())

    return response
def mycancel_order(request,id):     
    myorder =Order.objects.get(id__exact=id)    
    myorder.status = 'Cancelled'
    myorder.save()
    return HttpResponse("Cancelled")
def make_default(request,id):    
    if 'user_id' in request.session: 
      Shipping_Address.objects.filter(user=request.session['user_id']).update(is_default=False) 
      ship_de = Shipping_Address.objects.get(id=id,user=request.session['user_id'])
      ship_de.is_default=True
      ship_de.save()       
      return HttpResponse(status=204)
def remove_add(request,id):    
    if 'user_id' in request.session: 
      ship_de = Shipping_Address.objects.get(id=id)
      ship_de.is_active=False
      ship_de.save()     
      
      return redirect(checkt_add)  
      
def add_wishlist(request,id):
    product = Product.objects.get(id=id)    
    if 'user_id' in request.session: 
        try :
            uss = Users.objects.get(id=request.session['user_id'])  
            wishlist= Wishlist.objects.get( user = uss) 
            try :
                wishlist_item = WishlistItem.objects.get(product=product , wishlist = wishlist)
            except WishlistItem.DoesNotExist:     
                wishlist_item = WishlistItem.objects.create(
                    product=product,
                    wishlist = wishlist,
                    )
        except Wishlist.DoesNotExist:
            wishlist=Wishlist.objects.create( user = uss) 
            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist = wishlist,
            )     
            wishlist.save() 
            wishlist_item.save()  
        
            
    return redirect('wishlist')
def wishlist(request):
    if 'user_id' in request.session:    
        uss = Users.objects.get(id=request.session['user_id'])  
        wishlist= Wishlist.objects.get( user = uss)   
        wishlistitem = WishlistItem.objects.filter(wishlist = wishlist)
        context = { 
                'wishlistitem':wishlistitem,'logo_light':logo_light
            }
        return render(request,'Profile/wishlist.html',context)
    else :
        
        return render(request,'Profile/wishlist.html')

def wishlist_remove(request,id):
    product = Product.objects.get(id = id )
    uss = Users.objects.get(id=request.session['user_id']) 
    wishlist= Wishlist.objects.get( user = uss)  
    print("wwwwwwww",wishlist)
    print("ppppppp",product.id)
    wishlist_item = WishlistItem.objects.get(product=product.id , wishlist = wishlist)
    print(wishlist_item)
    wishlist_item.delete()
    return HttpResponse(status=204)
def myprofile(request):    
    user= Users.objects.get(id=request.session['user_id'])
    return render(request,'Profile/profile.html',{'user':user,'logo_light':logo_light})
def profile_edit(request):
    if request.method=='POST':
        alt_Phone_number=request.POST['phno2']
        location=request.POST['location']
        date_of_birth=request.POST['dob']
        gender=request.POST['gender']
        email=request.POST['email']
        Phone_number=request.POST['Phone_number']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        user= Users.objects.get(id=request.session['user_id'])
        user.first_name = first_name                   
        user.last_name = last_name
        user.Phone_number = Phone_number
        user.email = email
        user.username = email
        user.gender = gender
        user.date_of_birth = date_of_birth
        user.location = location
        user.alt_Phone_number = alt_Phone_number
        user.save()   
        return redirect('myprofile')
    user= Users.objects.get(id=request.session['user_id'])
    return render(request,'Profile/profile_up.html',{'user':user,'x':'Female','y':'Male'})
def change_password(request):
    if request.method=='POST':
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        confirm_new_password=request.POST['confirm_new_password']
        user= Users.objects.get(id=request.session['user_id'])
        if confirm_new_password==new_password:
            if confirm_new_password==new_password=='':
                messages.info(request,'Please fill password') 
                redirect(change_password)                  
            elif user.password==old_password:
                user.password=new_password
                user.save()
                redirect(myprofile)
                messages.info(request,'New Password Saved')
                
            else:
                messages.info(request,'Please fill old password') 
                redirect(change_password)  
        else:
            messages.info(request,'Passwords are not matching') 
            redirect(change_password)                       
    return render(request,'Profile/change_password.html',{'logo_light':logo_light})
def coupon_list(request):
    coupons = Coupon.objects.all()
    context={ 
        'coupons':coupons,
        'logo_light':logo_light
    }
    return render(request,'Profile/coupon_list.html',context)

    

     

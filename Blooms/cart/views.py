import json
import datetime
import razorpay
from google_currency import convert  
from Blooms.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from django.shortcuts import  redirect, render, get_object_or_404
from django.http import HttpResponse
from order.models import Order,Order_Product,Payment,Product_off
from product.models import Product
from admin_p.models import Users,Shipping_Address
from . models import Cart, Coupon ,cartItem
from content.models import Content
from user_sec.views import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
logo_light= Content.objects.get(name='logo_light')
def _cart_id(request):
    carts = request.session.session_key
    if not carts:
        carts = request.session.create()
    return carts
def add_cart(request):    
    z=False
    q = int(request.POST['qu'])
    product = Product.objects.get(id=request.POST['idd'])
    #current =request.session.session_key
    print("now i am on cart page")    
    if 'user_id' in request.session:            
        print(request.session['user_id'])   
        z=True  
        uss = Users.objects.get(id=request.session['user_id'])
        print(uss)   
        try: 
            carts = Cart.objects.get(user = uss)
        except Cart.DoesNotExist: 
            carts = Cart.objects.create(user = uss)
    else:
        try:
            carts = Cart.objects.get( carts_id = _cart_id(request) )  
        except Cart.DoesNotExist: 
            carts = Cart.objects.create( carts_id = _cart_id(request) ) 
    carts.save()
    
    if 'user_id' in request.session: 
        try :            
            cart_item = cartItem.objects.get(product=product , user = uss)
            cart_item.quantity +=  q
            cart_item.save()
        except cartItem.DoesNotExist:
            cart_item = cartItem.objects.create(
                product=product,
                quantity = q,
                cart = carts,
                user = uss,
            )
            cart_item.save()
    else :
        try :           
            cart_item = cartItem.objects.get(product=product.id,cart = carts )            
            cart_item.quantity += q
            cart_item.save()         
        except cartItem.DoesNotExist:
            cart_item = cartItem.objects.create(
                product=product,
                quantity = q,
                cart = carts,
            )
            cart_item.save()          
    return redirect('cart')

def apply_coupon(request):  
    if request.method=='POST':
        coupon_apply = request.POST['coupon_apply']   
        from_ = request.POST['from']       
             
        if 'user_id' in request.session:        
            uss = Users.objects.get(id=request.session['user_id'])     
            carts = Cart.objects.get(user = uss)
        else:
            carts = Cart.objects.get(carts_id = _cart_id(request)) 
        
        carts.coupon_applied=coupon_apply
        carts.save()  
        if from_=='cart':
            return redirect('cart')
        else:
            return redirect('checkt_add')       
def cart(request):    
    z=False        
    pro_off=Product_off.objects.all()                
    if 'user_id' in request.session: 
        z=True    
        uss = Users.objects.get(id=request.session['user_id'])     
        carts = Cart.objects.get(user = uss)          
        cart_items = cartItem.objects.filter(user=request.session['user_id']).order_by('product')          
        context = {
            'cart_items' : cart_items,'z':z,'logo_light':logo_light,'pro_off':pro_off
        }
        return render(request,'User/cart.html',context)
    else : 
        try:
            carts = Cart.objects.get(carts_id = _cart_id(request))            
            carts.save()
            cart_items = cartItem.objects.filter( cart = carts.id)
            context = {
                'cart_items' : cart_items,'z':z,'logo_light':logo_light,'pro_off':pro_off
             }
            return render(request,'User/cart.html',context)
        except:
            pass
        context = {
            'cart_items' : cart_items,'z':z,'logo_light':logo_light,'carts':carts,'pro_off':pro_off
        }
        return render(request,'User/cart.html',context) 
def update_cart(request,id):    
    q=request.GET['quantity'+str(id)]   
        
    if 'user_id' in request.session: 
        cart_item = cartItem.objects.get(id=id,user=request.session['user_id'])
        cart_item.quantity=q
        cart_item.save()
        return HttpResponse(status=204)
    else:
        carts = Cart.objects.get(carts_id = _cart_id(request))
        cart_item = cartItem.objects.get(id=id,  cart = carts)
        cart_item.quantity=q
        cart_item.save()
        return HttpResponse(status=204)
def delete_cart_product(request,id):    
    if 'user_id' in request.session: 
        cart_item = cartItem.objects.filter(id=id,user=request.session['user_id'])
        cart_item.delete()
        return HttpResponse(status=204)
    else:
        carts = Cart.objects.get(carts_id = _cart_id(request))
        cart_item = cartItem.objects.filter(id=id,  cart = carts)
        cart_item.delete()
        return HttpResponse(status=204)
    

def checkt_add(request):
    total = 0
    quantity = 0   
    i=True    
    coupons = Coupon.objects.all() 
    dis=0        
    if 'user_id' in request.session:     
        uss = Users.objects.get(id=request.session['user_id'])   
        carts = Cart.objects.get(user = uss) 
        try:
            coup = Coupon.objects.get(id = carts.coupon_applied)
            dis=coup.discount 
        except Coupon.DoesNotExist:
            pass         
        if carts is None:
            return redirect('cart')
        cart_items = cartItem.objects.select_related('product').filter(cart = carts)      
       
        tot_di=0     
        for cart_item in cart_items: 
            p=cart_item.product.price 
            q=cart_item.quantity  
            di=0          
            try:
                pro_off=Product_off.objects.get(product_id=cart_item.product.id)
                di=(p*pro_off.discount)/100
                tot_di+=(di*q)
                p=p-di
            except Product_off.DoesNotExist:
                pass         
            total += (p* cart_item.quantity)             
            quantity += cart_item.quantity
            if (quantity <= 0):
                return redirect('cart')
        
        if request.method == "POST":   
            first_name= request.POST['first_name'] 
            last_name= request.POST['last_name'] 
            phone_number = request.POST['Phone_number']
            email = request.POST['email']
            town = request.POST['add2']
            house = request.POST['add1']            
            state = request.POST['state']
            zip = request.POST['zip']  
            RadioDefault1=None
            try:
                 RadioDefault1 = request.POST["RadioDefault1"]
            except KeyError:
                RadioDefault1 = "None"
            if phone_number=='' or email=='' or house=='' or state=='' or town==''or zip==''or first_name=='':
                messages.info(request,'Please fill valid entries') 
                return redirect(checkt_add) 
            else:   
                if Shipping_Address.objects.filter(first_name = first_name,last_name=last_name,phone_number = phone_number,email = email,town = town,house = house,state = state,zip = zip).exists():
                    messages.info(request,'Shipping_Address Already exists')
                    return redirect(checkt_add)            
                else:                    
                    uss = Users.objects.get(id=request.session['user_id'])  
                    ship= Shipping_Address.objects.create(user=uss,first_name = first_name,last_name=last_name,phone_number = phone_number,email = email,town = town,house = house,state = state,zip = zip)
                    ship.save()
                    if RadioDefault1==True:                        
                        Shipping_Address.objects.filter(user=request.session['user_id']).update(is_default=False) 
                        ship_de = Shipping_Address.objects.get(id=ship.id)
                        ship_de.is_default=True
                        ship_de.save()   
                    print('Shipping_Address created')  
                    addresses=Shipping_Address.objects.filter(is_active=True,user=uss).order_by('-id')
                    return render(request,'Order/checkout_add.html',{'total' : total,'tot_di':tot_di,'quantity' : quantity,'z':True,'logo_light':logo_light,'addresses':addresses,'i':True,'coupons':coupons,'dis':dis,'coup_id':carts.coupon_applied})
        else: 
            addresses=Shipping_Address.objects.filter(is_active=True,user=uss).order_by('-is_default') 
            i=True 
            print(addresses)
            if addresses is not None:
                i=False                       
            return render(request,'Order/checkout_add.html',{'total' : total,'tot_di':tot_di,'quantity' : quantity,'z':True,'logo_light':logo_light,'addresses':addresses,'i':i,'coupons':coupons,'dis':dis,'coup_id':carts.coupon_applied})
    return redirect(login)        
def checkt_pay(request): 
   
    total = 0
    quantity = 0
    name=''
    email=''
    phno=''
    if request.method == "POST":         
        if request.POST['addid']=='':
            messages.info(request,'Please Select Delivery Address ')
            return redirect(checkt_add)           
        request.session['addid']=request.POST['addid']
        print("addresses", request.session['addid'])    
    if 'user_id' in request.session:    
        global iddd ,addid
        iddd= request.session['user_id'] 
        addid=request.session['addid']
        uss = Users.objects.get(id=request.session['user_id']) 
        name=uss.first_name
        email=uss.username
        phno=uss.Phone_number 
        carts = Cart.objects.get(user = uss)          
        cart_items = cartItem.objects.select_related('product').filter(cart = carts)            
        tot_di=0     
        for cart_item in cart_items: 
            p=cart_item.product.price 
            q=cart_item.quantity  
            di=0          
            try:
                pro_off=Product_off.objects.get(product_id=cart_item.product.id)
                di=(p*pro_off.discount)/100
                tot_di+=(di*q)
                p=p-di
            except Product_off.DoesNotExist:
                pass         
            total += (p* cart_item.quantity)             
            quantity += cart_item.quantity
        try:
            coup = Coupon.objects.get(id = carts.coupon_applied)
            dis=coup.discount 
            total=total-((total*dis)/100)
        except Coupon.DoesNotExist:
            pass 
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
        
        tot=total*100    
        
        DATA = {
            "amount": tot,
            "currency": "INR",
            "payment_capture":1        
        }
        payment_order=client.order.create(data=DATA)
        payment_order_id=payment_order['id']  
        y=convert('inr', 'usd', 1)      
        t= json.loads(y)
        am=float(t["amount"])
        total*= am; 
        fl=float(total)
        total=round(fl, 2)
        
        return render(request,'Order/payment_select.html',{'total' : total,'tot_di':tot_di,'quantity' : quantity,'z':True,'logo_light':logo_light,'api_key':RAZORPAY_KEY_ID,'order_id':payment_order_id,'name':name,'email':email,'phno':phno,})         
def show_addresses(request):    
    uss = Users.objects.get(id=request.session['user_id'])  
    addresses= Shipping_Address.objects.filter(user=uss,is_active=True,is_default=False)
    a=""
    for x in addresses:
        a+="<div class='card card-4'><div class='card__icon'><i class='fas fa-bolt'></i></div><p class='card__exit'><i class='fas fa-times'></i></p><h2 class='card__title'> "+x.house+","+x.town+"</h2><p class='card__apply'><a class='card__link' href='#'>Apply Now <i class='fas fa-arrow-right'></i></a></p></div>"
    return HttpResponse(a)   
def paypal_success(request):  
    total = 0
    quantity = 0   
    coup_discount=0        
    print('in')  
    uss = Users.objects.get(id=iddd) 
    carts = Cart.objects.get(user = uss)          
    cart_items = cartItem.objects.select_related('product').filter(cart = carts)            
    tot_di=0     
    for cart_item in cart_items: 
        p=cart_item.product.price 
        q=cart_item.quantity  
        di=0          
        try:
            pro_off=Product_off.objects.get(product_id=cart_item.product.id)
            di=(p*pro_off.discount)/100
            tot_di+=(di*q)
            p=p-di
        except Product_off.DoesNotExist:
            pass         
        total += (p* cart_item.quantity)             
        quantity += cart_item.quantity      
    try:
        coup = Coupon.objects.get(id = carts.coupon_applied)
        dis=coup.discount 
        coup_discount=(total*dis)/100
    except Coupon.DoesNotExist:
        coup_discount=0       
    order_total = round(total-coup_discount)
    payment_method='PAYPAL'
    ship=Shipping_Address.objects.get(id=addid)                      
    pay = Payment.objects.create(payment_method=payment_method,amount_paid=order_total,status="Completed")
    pay.save()
    order=Order.objects.create(payment_id=int(pay.id),address=ship,user=uss, order_total = order_total)
    order.save()       
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))) 
    order.order_number = order_id_generated  
    order.save()             
    for cart_item in cart_items:   
        di=0
        p=cart_item.product.price           
        try:
            pro_off=Product_off.objects.get(product_id=cart_item.product.id)
            di=pro_off.discount
            p=p-(p*di)/100  
        except Product_off.DoesNotExist:
            pass             
        order_item = Order_Product.objects.create(product=cart_item.product,discount=di,discount_price=p,quantity = cart_item.quantity,order = order,product_price=cart_item.product.price)
        order_item.save() 
    cart_items.delete() 
    carts.delete()  
    context = {'z':True,'logo_light':logo_light,}
    return render(request,'Order/pay_success.html',context)
@csrf_exempt
def pay_success(request):  
    total = 0
    quantity = 0           
    print('in')  
    uss = Users.objects.get(id=iddd) 
    carts = Cart.objects.get(user = uss)          
    cart_items = cartItem.objects.select_related('product').filter(cart = carts)            
    tot_di=0     
    for cart_item in cart_items: 
        p=cart_item.product.price 
        q=cart_item.quantity  
        di=0          
        try:
            pro_off=Product_off.objects.get(product_id=cart_item.product.id)
            di=(p*pro_off.discount)/100
            tot_di+=(di*q)
            p=p-di
        except Product_off.DoesNotExist:
            pass         
        total += (p* cart_item.quantity)             
        quantity += cart_item.quantity
    try:
        coup = Coupon.objects.get(id = carts.coupon_applied)
        dis=coup.discount 
        coup_discount=(total*dis)/100
    except Coupon.DoesNotExist:
        coup_discount=0            
    order_total = round(total-coup_discount)
    payment_method='RAZOR_PAY'
    ship=Shipping_Address.objects.get(id=addid)                      
    pay = Payment.objects.create(payment_method=payment_method,amount_paid=total,status="Completed")
    pay.save()
    order=Order.objects.create(payment_id=int(pay.id),address=ship,user=uss, order_total = order_total)
    order.save()       
    order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))) 
    order.order_number = order_id_generated  
    order.save()             
    for cart_item in cart_items:                 
        order_item = Order_Product.objects.create(product=cart_item.product,quantity = cart_item.quantity,order = order,product_price=cart_item.product.price)
        order_item.save() 
    cart_items.delete() 
    carts.delete()  
    context = {'z':True,'logo_light':logo_light,}
    return render(request,'Order/pay_success.html',context)
def cash_on_delivery(request):
    total = 0
    quantity = 0   
    coup_discount=0
    if 'user_id' in request.session:      
        print('in') 
        uss = Users.objects.get(id=request.session['user_id']) 
        carts = Cart.objects.get(user = uss)          
        cart_items = cartItem.objects.select_related('product').filter(cart = carts)            
        tot_di=0     
        for cart_item in cart_items: 
            p=cart_item.product.price 
            q=cart_item.quantity  
            di=0          
            try:
                pro_off=Product_off.objects.get(product_id=cart_item.product.id)
                di=(p*pro_off.discount)/100
                tot_di+=(di*q)
                p=p-di
            except Product_off.DoesNotExist:
                pass         
            total += (p* cart_item.quantity)             
            quantity += cart_item.quantity
        try:
            coup = Coupon.objects.get(id = carts.coupon_applied)
            dis=coup.discount 
            coup_discount=(total*dis)/100
        except Coupon.DoesNotExist:
            coup_discount=0            
        order_total = round(total-coup_discount)
        payment_method='COD'
        ship=Shipping_Address.objects.get(id=request.session['addid'])                      
        pay = Payment.objects.create(payment_method=payment_method,amount_paid=total,status="pending")
        pay.save()
        order=Order.objects.create(payment_id=int(pay.id),address=ship,user=uss, order_total = order_total)
        order.save()       
        order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))) 
        order.order_number = order_id_generated  
        order.save()             
        for cart_item in cart_items:                 
            order_item = Order_Product.objects.create(product=cart_item.product,quantity = cart_item.quantity,order = order,product_price=cart_item.product.price)
            order_item.save() 
        cart_items.delete() 
        carts.delete()    
        context = {
        'z':True,'logo_light':logo_light,
        }
        return render(request,'Order/Place_order.html',context)  
       

        
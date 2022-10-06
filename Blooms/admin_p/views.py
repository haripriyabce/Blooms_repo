import csv
from decimal import Subnormal
import os
import tempfile
import calendar
from django.db.models import Sum,Count
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import loader
from admin_p.models import Users,Shipping_Address
from order.models import Order,Order_Product, Payment,Product_off
from category.models import Category,Subcategory
from product.models import Product,Product_cate,Offer
from product.forms import ProductForm
from django.core.paginator import Paginator
import datetime
from django.template.loader import render_to_string
from cart.models import Coupon
import xlwt
from weasyprint import HTML
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):    
    if 'admin_username' in request.session:
        return redirect(home)         
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None and user.is_superuser:
            request.session['admin_username'] = username
            return redirect(home)
        else:
            messages.info(request,'invalid credentials')
            return redirect(login)    
    return render(request,'Admin/auth-login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def home(request):
    if 'admin_username' in request.session:  
        completed_order = Order.objects.filter(status='Completed').count()
        pending_order = Order.objects.filter(status='Pending').count()        
        cancelled_order = Order.objects.filter(status='Cancelled').count()   
        cancelled_order = Order.objects.filter(status='Cancelled').count() 
        order_status_count=Order.objects.values('status').order_by().annotate(status_count=Count('status')).order_by('-status_count')[:5]
          
        order_count = Order.objects.all().count()        
        recent_order = Order.objects.select_related('address').select_related('payment').order_by('-created_at')[:5]     
        payment_method_count=Order.objects.values('payment__payment_method').order_by().annotate(payment_method_count=Count('payment__payment_method')).order_by('-payment_method_count')[:5]
       
        top_products=Product.objects.annotate(quantity_sum=Sum('order_product__quantity')).filter(quantity_sum__gt=0).order_by('-quantity_sum')[:5]
        print(top_products)
        template = loader.get_template('Admin/admin_home.html')
        context = {  
        'order_count':order_count,
        'completed_order':completed_order,
        'pending_order':pending_order,
        'cancelled_order':cancelled_order,
        'recent_order':recent_order, 
        'top_products' :top_products,
        'payment_method_count':payment_method_count,  
        'order_status_count':order_status_count   
        }
        return HttpResponse(template.render(context, request))
    return redirect(login)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'admin_username' in request.session:
        request.session.flush()    
    return redirect(login)

def user(request):
    users= Users.objects.all().order_by('-id') 
    if request.method == 'POST':        
        search = request.POST["user_search"] 
        users = Users.objects.filter(first_name__icontains = search)    
    paginator = Paginator(users, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render( request,'Admin/user_list.html',{'page_obj':page_obj}) 
def block_unblock(request,id):
    user =Users.objects.get(id__exact=id)
    if user.is_active==True:
        user.is_active = False
        user.save()
        return HttpResponse("User Blocked")
    else:
        user.is_active = True
        user.save()
        return HttpResponse("User Unblocked") 
def category(request):
    categories=Category.objects.all().order_by('-id') 
    paginator = Paginator(categories, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render( request,'Admin/category_list.html',{'page_obj':page_obj})    



def add_cate(request):  
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        if name=='' or description=='' :
            messages.info(request,'Please fill valid entries') 
            return redirect(add_cate) 
        else:   
            if Category.objects.filter(category_name=name).exists():
                messages.info(request,'Category Already exists')
                return redirect(add_cate)            
            else:   
                cate= Category.objects.create(category_name=name,slug=name,description=description,category_image=image)
                cate.save()
                print('category created')
                return redirect(category)             
    else:
        return render(request,'Admin/Add_category.html')  

def update_cat(request,id): 
    if 'admin_username' in request.session:
        if request.method == 'POST':        
            name = request.POST['name']
            description = request.POST['description']        
            if name=='' or description=='':
                messages.info(request,'Please fill valid entries')            
                return redirect(update_cat(id))
            else:
                cat = Category.objects.get(id=id)
                cat.category_name = name
                cat.description = description
                cat.save()
                return redirect(category)          
        mycat = Category.objects.get(id=id) 
        template = loader.get_template('Admin/up_category.html')
        context = { 'mycat': mycat, }
        return HttpResponse(template.render(context, request))
def deactivate_cat(request,id):    
    #cate = Category.objects.get(id=id)
    mycat =Category.objects.get(id__exact=id)
    if mycat.status==0:
        mycat.status = 1
    else:
        mycat.status = 0
    mycat.save()
    return HttpResponse("Status Changed")

def subcategory(request):
    subcategories=Subcategory.objects.select_related('category').all().order_by('-id')
    
    paginator = Paginator(subcategories, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render( request,'Admin/subcategory_list.html',{'page_obj':page_obj})    
def add_subcate(request):  
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        description = request.POST['description']
        
        if name=='' or description=='' :
            messages.info(request,'Please fill valid entries') 
            return redirect(add_subcate) 
        else:   
            if Subcategory.objects.filter(subcategory_name=name).exists():
                messages.info(request,'Subcategory Already exists')
                return redirect(add_subcate)            
            else:   
                sub= Subcategory.objects.create(subcategory_name=name,category_id=category,slug=name,description=description)
                sub.save()
                print('subcategory created')
                return redirect(subcategory)             
    else:
        categories=Category.objects.all()
        context={'categories':categories}
        template = loader.get_template('Admin/Add_subcategory.html')        
        return HttpResponse(template.render(context, request))
        
def update_subcat(request,id): 
    if 'admin_username' in request.session:
        if request.method == 'POST':        
            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']        
            if name=='' or category=='' or description=='':
                messages.info(request,'Please fill valid entries')            
                return redirect(update_subcat(id))
            else:
                subcat = Subcategory.objects.get(id=id)
                subcat.subcategory_name = name
                subcat.description = description
                subcat.category_id = category
                subcat.save()
                return redirect(subcategory)          
        mysubcat = Subcategory.objects.get(id=id) 
        categories=Category.objects.all()
        template = loader.get_template('Admin/up_subcategory.html')
        context = { 'mysubcat': mysubcat,'categories':categories }
        return HttpResponse(template.render(context, request))
def deactivate_sub(request,id):       
    mysub=Subcategory.objects.get(id__exact=id)
    if mysub.status==True:
        mysub.status = False
    else:
        mysub.status = True
    mysub.save()
    return HttpResponse("Status Changed")

def product_delete(request,id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('products')
def add_products(request): 
    if request.method == 'POST':
        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST.get('stock')
        slug = request.POST['slug']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        subcat=request.POST.getlist('subcat')             
        if stock=='':
            stock=0
        prod=Product.objects.create(product_name=product_name,stock=stock,description=description,price=price,category_id=1,slug=slug,image1=image1,image2=image2,image3=image3)
        prod.save()        
        i=Product.objects.order_by('-id')[0]        
        for f in subcat:            
            sub=Subcategory.objects.get(id=f)    
            cid=sub.category_id   
            cat=Category.objects.get(id=cid)     
            Prod_cat=Product_cate.objects.create(catid=cat,subcategory=sub,product=i)
            Prod_cat.save()
        print("product created")           
        messages.info(request,'Product added successfully')
        return redirect('products')  
    categories =Category.objects.all()
    subcategories=Subcategory.objects.all()    
    context={'subcategories':subcategories,'categories':categories}
    template = loader.get_template('Admin/add_product.html')
    return HttpResponse(template.render(context, request))
      
def product_edit(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST.get('stock')
        slug = request.POST['slug']
        # image1 = request.FILES['image1']
        # image2 = request.FILES['image2']
        # image3 = request.FILES['image3']
        subcat=request.POST.getlist('subcat')
        pro = Product.objects.get(id=id)
        for f in subcat:
            sub=Subcategory.objects.get(id=f)    
            cid=sub.category_id   
            cat=Category.objects.get(id=cid)     
            Prod_cat=Product_cate.objects.create(catid=cat,subcategory=sub,product=pro)
            Prod_cat.save()
       
        if len(product_name)>0:
            pro.product_name=product_name                    
        if len(description)>0:
            pro.description=description
        if len(price)>0:
            pro.price=price
        if len(stock)>0:
            pro.stock=stock
        
        # if request.FILES['image1']!='':
        #     os.remove(pro.image1.path)
        #     pro.image1 = image1
        # if len(image2)>0:
        #     os.remove(pro.image2.path)
        #     pro.image2 = image2
        # if len(image3)>0:
        #     os.remove(pro.image3.path)
        #     pro.image3 = image3
        pro.save()           
        messages.success(request,'Product edited successfully')
        return redirect('products')
    else:
        categories =Category.objects.all()
        subcategories=Subcategory.objects.all() 
        return render (request,'Admin/up_product.html',{'subcategories':subcategories,'categories':categories,'product':product})
    
def products(request):
    products= Product.objects.all().order_by('-id')
    if request.method == 'POST':
        search = request.POST["product_search"] 
        products = Product.objects.filter(product_name__icontains = search).order_by('-id')
        
    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    return render( request,'Admin/product_list.html',{'page_obj':page_obj})
def rep_products(request):
    products=Product.objects.annotate(quantity_sum=Sum('order_product__quantity')).filter(quantity_sum__gt=0).order_by('-quantity_sum')[:5]
       
    if request.method=='POST':        
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')  
        year = request.POST.get('yearly')
        month = request.POST.get('monthly')  
        if from_date !='' and to_date!='':
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            products=Product.objects.annotate(quantity_sum=Sum('order_product__quantity')).filter(created_at__date__range=[from_date, to_date]) 
        if  year !='': 
            products=Product.objects.annotate(quantity_sum=Sum('order_product__quantity')).filter(created_at__year__gte=year,created_at__year__lte=year) 
        if  month !='':      
            datetime_object = datetime.datetime.strptime(month, "%B")
            month = datetime_object.month
            products=Product.objects.annotate(quantity_sum=Sum('order_product__quantity')).filter(created_at__month__gte=month,created_at__month__lte=month) 
        
        
    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    mon=list(calendar.month_name)
    e=range(2011,2023)
    return render( request,'Admin/products_report.html',{'page_obj':page_obj,'e':e,'mon':mon}) 
def profile(request):
    return render(request,'Admin/profile.html')
def orders(request):
    orders=Order.objects.select_related('address').select_related('payment').order_by('-id')    
    paginator = Paginator(orders, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render( request,'Admin/order_list.html',{'page_obj':page_obj})
def rep_orders(request): 
    orders=Order.objects.select_related('address').select_related('payment').order_by('-id')   
    if request.method=='POST':        
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')  
        year = request.POST.get('yearly')
        month = request.POST.get('monthly')  
        if from_date !='' and to_date!='':
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            orders = Order.objects.filter(created_at__date__range=[from_date, to_date]) 
        if  year !='': 
            orders = Order.objects.filter(created_at__year__gte=year,created_at__year__lte=year) 
        if  month !='':      
            datetime_object = datetime.datetime.strptime(month, "%B")
            month = datetime_object.month
            orders = Order.objects.filter(created_at__month__gte=month,created_at__month__lte=month) 
            
    #orders=Order.objects.select_related('address').select_related('payment').order_by('-id')    
    paginator = Paginator(orders, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mon=list(calendar.month_name)
    e=range(2011,2023)
    
    return render( request,'Admin/orders_report.html',{'page_obj':page_obj,'e':e,'mon':mon})       
def rep_orders_yearly(request): 
    orders=Order.objects.select_related('address').select_related('payment').order_by('-id')   
    if request.method=='POST':        
        year = request.POST.get('yearly')
        print(year)
       
    #orders = Order.objects.filter(created_at__date__range=[from_date, to_date])    
    #orders=Order.objects.select_related('address').select_related('payment').order_by('-id')    
    paginator = Paginator(orders, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mon=list(calendar.month_name)
    e=range(2011,2023)
    return HttpResponse('rghh')
    #return render( request,'Admin/orders_report.html',{'page_obj':page_obj,'e':e,'mon':mon})           
def orders_de(request,id):
    order=Order.objects.select_related('address').select_related('payment').get(id=id)
    orderitems=Order_Product.objects.select_related('product').filter(order_id=id)       
    return render( request,'Admin/orderitem_list.html',{'order':order,'orderitems':orderitems}) 
def cancel_order(request,id):     
    myorder =Order.objects.get(id__exact=id)    
    myorder.status = 'Cancelled'
    myorder.save()
    return HttpResponse("Cancelled")
def complete_order(request,id):     
    myorder =Order.objects.get(id__exact=id)    
    myorder.status = 'Delivered'
    myorder.save()
    return HttpResponse("Delivered")
def out_for_delivery(request,id):     
    myorder =Order.objects.get(id__exact=id)    
    myorder.status = 'Out for Delivery'
    myorder.save()
    return HttpResponse("Out for Delivery")
def ship(request,id):     
    myorder =Order.objects.get(id__exact=id)    
    myorder.status = 'Shipped'
    myorder.save()
    return HttpResponse("Shipped")

def offer(request):
    offer=Product_off.objects.select_related('product').order_by('-id') 
    paginator = Paginator(offer, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render( request,'Admin/offer_list.html',{'page_obj':page_obj})   

def add_offer(request):  
    if request.method == 'POST':
        name = request.POST['name']         
        discount = request.POST['discount']
        if name=='' :
            messages.info(request,'Please fill valid entries') 
            return redirect(add_offer) 
        else:   
            if Product_off.objects.filter(product_id=name).exists():
                messages.info(request,'Offer Already exists')
                return redirect(add_offer)            
            else:   
                cate= Product_off.objects.create(product_id=name,discount=discount)
                cate.save()
                print('Offer created')
                return redirect(offer)             
    else:
        product=Product.objects.all().order_by('product_name')
        return render(request,'Admin/Add_offer.html',{'pro':product})  

def update_offer(request,id): 
    if 'admin_username' in request.session:
        if request.method == 'POST':        
            name = request.POST['name']
            description = request.POST['description']        
            if name=='' or description=='':
                messages.info(request,'Please fill valid entries')            
                return redirect(update_cat(id))
            else:
                cat = Category.objects.get(id=id)
                cat.category_name = name
                cat.description = description
                cat.save()
                return redirect(offer)          
        mycat = Category.objects.get(id=id) 
        template = loader.get_template('Admin/up_category.html')
        context = { 'mycat': mycat, }
        return HttpResponse(template.render(context, request))
def deactivate_offer(request,id):    
    #cate = Category.objects.get(id=id)
    mycat =Category.objects.get(id__exact=id)
    if mycat.status==0:
        mycat.status = 1
    else:
        mycat.status = 0
    mycat.save()
    return HttpResponse("Status Changed")




def report_date(request):  
      
    search=request.GET['date_from']     
    #myorder =Order.objects.filter(date__range=["2011-01-01", "2011-01-31"])    
    return HttpResponse(search)


def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['order ','name ','amount  ','date'])

    salesreport = Order.objects.all()

    for order in salesreport:
        writer.writerow([order.order_number , order.first_name , order.order_total  , order.created_at ])
    return response

def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style =xlwt.XFStyle()
    font_style.font.bold =True

    columns = ['order ','name ','amount  ','date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num, columns[col_num],font_style)
    
    font_style= xlwt.XFStyle()

    rows = Order.objects.all().values_list('order_number','first_name','order_total','created_at')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]),font_style)

    wb.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachement; filename=SalesReport' +str(datetime.datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'
    orders=Order.objects.select_related('address').select_related('payment').order_by('-id')
   
    # if request.method=='POST':        
    #     from_date = request.POST.get('from_date')
    #     to_date = request.POST.get('to_date')    
    #     if from_date !='' and to_date!='':
    #         from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
    #         to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')

    #         orders = Order.objects.filter(created_at__date__range=[from_date, to_date])

    salesreport = Order.objects.select_related('address').select_related('payment').order_by('-id')
    total= salesreport.aggregate(Sum('order_total'))

    html_string = render_to_string('admin/pdf_output.html',{ 'salesreport':salesreport, 'total': total})

    html=HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output : 
        output.write(result)
        output.flush()
        #output=open(output.name,'rb')
        output.seek(0)
        response.write(output.read())

    return response
def coupon_list(request):
    coupons = Coupon.objects.all()
    context={ 
        'coupons':coupons
    }
    return render(request,'admin/coupon_list.html',context)

def coupon_disable(request,id):
    
    coupon = Coupon.objects.get(id=id)
    print(coupon)
    if coupon.active == True:
        coupons = Coupon.objects.filter(id=id)
        coupons = coupons.update(active = False)
        
        return redirect('coupon_list')
    
    elif coupon.active == False:
         coupons = Coupon.objects.filter(id=id)
         coupons = coupons.update(active = True)
        
         return redirect('coupon_list')

def coupon_edit(request,id):
    coupon_id = id
    if request.method == 'POST':
        if Coupon.objects.filter(id=coupon_id).exists():
            offr = Coupon.objects.filter(id=coupon_id)
            offer = request.POST['discount']
            coupon_code = request.POST['coupon_code'] 
            valid_from = request.POST['valid_from'] 
            valid_till = request.POST['valid_till'] 
            min_purchase = request.POST['min_purchase'] 
            
            
            offr.update(discount = offer, coupon_code = coupon_code,valid_from = valid_from, valid_to = valid_till,min_purchase=min_purchase)
            
            return redirect('coupon_list')
    else:
        coupon = Coupon.objects.get(id=coupon_id)
        context = { 
            'coupon_id' : coupon_id,
            'coupon': coupon
        }
        return render(request,'admin/coupon_edit.html',context)

def coupon_add(request):
    if request.method == 'POST':       
        offer = request.POST['discount']
        coupon_code = request.POST['coupon_code'] 
        valid_from = request.POST['valid_from'] 
        valid_till = request.POST['valid_till'] 
        min_purchase = request.POST['min_purchase']             
        print(offer)            
        coupon = Coupon.objects.create(discount = offer, coupon_code = coupon_code,valid_from = valid_from, valid_to = valid_till,min_purchase=min_purchase)
        coupon.save() 
        return redirect('coupon_list')
    else : 
        return render(request,'admin/coupon_add.html')

   
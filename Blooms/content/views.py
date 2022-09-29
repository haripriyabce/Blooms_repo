import os
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Content
from django.core.paginator import Paginator
# Create your views here.
def content(request):
    contents=Content.objects.all()    
    
    paginator = Paginator(contents, 3) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Admin/content_list.html', {'page_obj': page_obj,'contents':contents})
       
def add_content(request):  
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        if name=='' or description=='' :
            messages.info(request,'Please fill valid entries') 
            return redirect(add_content) 
        else:   
            if Content.objects.filter(name=name).exists():
                messages.info(request,'Content Already exists')
                return redirect(add_content)            
            else:   
                cate= Content.objects.create(name=name,description=description,image=image)
                cate.save()
                print('content created')
                return redirect(content)             
    else:
        return render(request,'Admin/Add_content.html') 
def update_content(request,id): 
    if 'admin_username' in request.session:
        if request.method == 'POST':        
            name = request.POST['name']
            description = request.POST['description']   
            image = request.FILES['image']     
            if name=='' or description=='':
                messages.info(request,'Please fill valid entries')            
                return redirect(update_content(id))
            else:
                con = Content.objects.get(id=id)
                con.name = name
                con.description = description
                if image !='':
                    os.remove(con.image.path)
                    con.image = image
                con.save()
                return redirect(content)          
        mycon = Content.objects.get(id=id)         
        context = { 'mycon': mycon, }
        return render(request,'Admin/up_content.html',context)
        
    
def deactivate_content(request,id):    
    #cate = Content.objects.get(id=id)
    mycat =Content.objects.get(id__exact=id)
    if mycat.status=='Active':
        mycat.status = 'InActive'
    else:
        mycat.status = 'Active'
    mycat.save()
    return HttpResponse("Status Changed")


 
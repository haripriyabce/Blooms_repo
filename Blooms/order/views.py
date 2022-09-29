from django.shortcuts import render

# Create your views here.
def checkt(request):
    return render(request,'User/checkout.html')
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.

def index(request):
      context = {}
      return render(request, 'store/index.html', context)

def home(request):
      context = {}
      return render(request, 'store/home.html', context)

def loginUser(request):
      if request.method == 'POST':
           username = request.POST.get('username')
           password = request.POST.get('password')
           if username and password:
                user = authenticate(username=username, password=password)

                if user is not None:
                     login(request, user)
                     return redirect('home')
                else:
                     messages.error(request, 'Username or password is incorrect.')
                     
           else:
                messages.error(request, 'Fill out all the fields')

      return render(request, 'store/login.html', {})

def register(request):
      form = RegisterForm()
      if request.method == 'POST':
           form = RegisterForm(request.POST)
           if form.is_valid():
                form.save()
                return redirect('login')
      else:
           form = RegisterForm()
      return render(request, 'store/register.html', {'form':form})

def logoutUser(request):
      context = {}
      return render(request, 'store/logout.html', context)

def shop(request):
     products = Product.objects.all()
     context = {'products':products}
     return render(request, 'store/shop.html', context)

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total': 0, 'get_cart_items':0}
     context = {'items':items, 'order':order}
     return render(request, 'store/cart.html', context)

def checkout(request):
      if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
      else:
          items = []
          order = {'get_cart_total': 0, 'get_cart_items':0}
      context = {'items':items, 'order':order}

      return render(request, 'store/checkout.html', context)

def index(request):
      context = {}
      return render(request, 'store/index.html', context)


     
def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('productId:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity -1)
     
     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)
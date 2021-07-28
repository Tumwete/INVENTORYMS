from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

@login_required(login_url='user-login')  # we write the logic for make orders here because staff index is inside the index.html page
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) #form has been validated bt with commit=False, we havent saved it yet
            instance.staff = request.user #whichever user has made e request is who we are asigning the particular item to
            instance.save()
            product = form.cleaned_data.get('name')
            messages.success(request, f'{product} has been added')
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required(login_url='user-login')
def staff_detail(request, pk): #because you want to view the details of a particular member of staff
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html',context)

@login_required(login_url='user-login')
def product(request):
    items = Product.objects.all()
    product_count = items.count()
    workers_count = User.objects.all().count() #counts all the items from the product model
    orders_count = Order.objects.all().count()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/product.html', context)


@login_required(login_url='user-login')
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/order.html', context)



@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required(login_url='user-login')
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')

    else:
        form = ProductForm(instance=item)
        context = {
            'form': form,

            }
    return render(request, 'dashboard/product_update.html',context)
from django.shortcuts import render , reverse
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import json
import requests
from django.core.paginator import Paginator
from django.db.models import Max,Min,Count

from django.template.loader import render_to_string

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .serializers import *

from .models import *
from .forms import *

link = "http://127.0.0.1:8000"
# link = "http://192.168.0.103:8000"

def cart(request):
    total = 0

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        total = order.get_cart_total()
        quantity = order.get_cart_items()
    else:
        items = []
        quantity = 0
        total = 0


    return render(request, "App1/cart.html", {
    "order" : items,
    "total" : total,
    "quantity" : quantity

    })

def index(request) :

    # cart_items = cart(request)
    products = product.objects.all().order_by('-id')[:6]
    cat = Category.objects.all()
    return render(request, "App1/index.html",{'data':products, 'categories':cat})

@register.filter        # Decorator 
def get(d,key):         # Dictionary filter 
    return d.get(key)


def shop(request,brand="",ref=""):
    # cart_items = cart(request)
    # response = requests.get('http://127.0.0.1:8000/api/products')
    # data = response.json()

    categories = Category.objects.all()
    sizes = Variant.objects.all().values("size").distinct().order_by("size")

    brands = Brand.objects.all()
    
    # .values("Marca").distinct().order_by("Marca")

    return render(request,"App1/shop.html"
    ,{    
        "categories" : categories,
        "brands": brands,
        "ref" : ref,
        "sizes" : sizes,
        "host" : link
    })

def productos(request,cat,url):
    products = product.objects.get(url=url)

    # size = Variant.objects.filter(parent=products).values("size").distinct()
    # sizes = sorted(i['size'] for i in size)
    
    color = Variant.objects.filter(parent=products).values("color").distinct()
    colors = [i['color'] for i in color]

    related_products = product.objects.filter(category=products.category).exclude(url=url)[:4]
    
    return render(request, "App1/product_detail.html",{
        "prd" : products,
        "colors" : colors,
        "data" : related_products,
    })

def login_view(request):

    if request.method == "POST":
    # Accessing username and password from form data         
        username = request.POST["username"]
        password = request.POST["password"]

    # Check if username and password are correct, returning User object if so         
        user = authenticate(request, username=username, password=password)

    # If user object is returned, log in and route to index page:         
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Otherwise, return login page again with new context         
        else:
            return render(request, "App1/login.html", {
                "message": "Invalid Credentials"
            })

    return render(request, "App1/login.html")

def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("index"))

def signup(request):
    form = CreateUserForm() # Imported from .forms
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}

    return render(request, "App1/signup.html",context)

def my_account(request):
    if request.user.is_authenticated:
        return render(request,"App1/my-account.html")
    else:
        return HttpResponseRedirect(reverse("login"))

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    color = data['color']
    size = data['size']

    customer = request.user.customer

    # only can be added Variant products not main products
    # to be check
    paren = product.objects.get(ref=productId)


    p = Variant.objects.get(parent=paren,color=color)

    qty = Quantity.objects.get(variant=p,size=size)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=p, size=size)

    if action == 'add':
        if qty.quantity > 0:
            qty.quantity -= 1
            orderItem.quantity = (orderItem.quantity + 1)
            orderItem.size = size
    elif action == 'remove':
        qty.quantity += 1
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def charge_sizes(request):
    
    productId = request.GET['id']
    color = request.GET['color']

    paren = product.objects.get(ref=productId)
    parent = Variant.objects.get(parent=paren,color=color)

    sizes = Quantity.objects.filter(variant=parent).values("size").distinct()

    sizes = sorted({i['size'] for i in sizes})
    
    print(Quantity.objects.filter(variant=parent).values("quantity"))
    return render(request, 'App1/sizes.html', {'sizes': sizes})

def stores(request):
    stores = store.objects.all()
    return render(request, 'App1/stores.html', {"stores" : stores})

###############################################################
## FILTERS


def tienda(request,cat="",ref="",sku=""):

    categories = Category.objects.all()
    # sizes = Variant.objects.all().values("size").distinct().order_by("size")
    sizes = Quantity.objects.all().values("size").distinct()
    brands = Brand.objects.all()
    
    # .values("Marca").distinct().order_by("Marca")

    products = product.objects.all().order_by('-id').distinct()

    if not cat=='':
        products = products.filter(category=cat)

    # paginator = Paginator(products, 2) 

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    min_price=product.objects.aggregate(Min('price'))
    max_price=product.objects.aggregate(Max('price'))

    departments = Department.objects.all()
    return render(request,"App1/tienda.html"
    ,{   
        "cat":cat,
        "data" : products,
        "categories" : categories,
        "brands": brands,
        "ref" : ref,
        "sku" : sku,
        "sizes" : sizes,
        "host" : link,
        "page_obj" :products,
        'min_price':min_price,
        'max_price':max_price,
        "departments":departments,
    })

def tienda2(request,cat):
    cat = Category.objects.get(url=cat)
    data = product.objects.filter(category=cat).distinct()
    
    return render(request,"App1/category_product_list.html",{"data":data,"cat":cat,})

def filter_data(request):
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    department=request.GET.getlist('department[]')
    sizes=request.GET.getlist('size[]')
    
    sort=request.GET.getlist('sort')
    sort = str(sort[0])
    # minPrice=request.GET['minPrice']
    # maxPrice=request.GET['maxPrice']
    allProducts=product.objects.all().order_by(sort).distinct()
    # allProducts=allProducts.filter(productattribute__price__gte=minPrice)
    # allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    # if len(colors)>0:
    # 	allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()

    if len(categories)>0:
        if '0' not in categories:
            allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(department)>0:
    	allProducts=allProducts.filter(department__id__in=department).distinct()

    # if len(sizes)>0:
    # 	allProducts=allProducts.filter(size__id__in=sizes).distinct()

    t=render_to_string('App1/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})

# Search
def search(request):
	q=request.GET['q']
	data = product.objects.filter(description__icontains=q).order_by('-id')
	return render(request,'App1/search.html',{'data':data})

def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=product.objects.filter(category=category).order_by('-id')
	return render(request,'App1/category_product_list.html',{
			'data':data,
			})

def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'App1/category_list.html',{'data':data})


    
def contact(request):
    return render(request,'App1/contact.html')

def checkout(request):
    total = 0

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        total = order.get_cart_total()
        quantity = order.get_cart_items()
    else:
        items = []
        quantity = 0
        total = 0

    return render(request,'App1/checkout.html', {
    "order" : items,
    "total" : total,
    "quantity" : quantity

    })
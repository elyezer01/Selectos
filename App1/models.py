from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    description = models.CharField(max_length=200, default=None)
    img = models.ImageField(default=None)
    url= models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.description)    #LOWERCASE
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.description
    
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

class Brand(models.Model):
    Marca = models.CharField(max_length=50,default=None)
    img = models.ImageField(default=None)

    def __str__(self):
        return self.Marca

class Department(models.Model):
    description = models.CharField(max_length=50)
    img = models.ImageField(default=None)

    def __str__(self):
        return self.description

class product(models.Model):    
    ref = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cat")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default='1')     ###FIX
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    url = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.description+"-"+self.ref)
        super(product, self).save(*args, **kwargs)

    def __str__(self):
        return self.ref


class Variant(models.Model):
    parent = models.ForeignKey(product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=10)
    img = models.ImageField(default=None)
    
    # def __str__(self):
    #     return "%s %s %s" % (self.parent.ref, self.color ,str(self.size))
    def __str__(self): 
        return "%s %s" % (self.parent.ref, self.color )
    
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

class Quantity(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    size = models.CharField(max_length=2)
    quantity = models.PositiveIntegerField(default=0)
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        return sum([item.get_total for item in orderitems])

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])

class OrderItem(models.Model):
    product = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True, blank=True, related_name="main")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=2, null=True,default="")

    @property
    def get_total(self):
        return self.product.parent.price * self.quantity

class store(models.Model):
    name = models.CharField(max_length=60, null=True)
    img = models.ImageField()
    description = models.CharField(max_length=180, null=True)

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url
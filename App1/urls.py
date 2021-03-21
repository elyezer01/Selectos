from django.urls import path

from . import views

urlpatterns = [
    path("", views.index , name="index"),
    path("productos", views.tienda , name="shop"),
    path("productos/<str:cat>", views.tienda2, name="shop"),
    path("productos/<str:cat>/<str:url>", views.productos, name="product"),


    path("categories", views.category_list, name="categories"),
    
    path("login", views.login_view , name="login"),
    path("sign-up", views.signup, name="signup"),
    path("logout", views.logout_view , name="logout"),
    path("my-account", views.my_account , name="my-account"),

    path("update-item/", views.updateItem , name="updateItem"),
    path("charge_sizes", views.charge_sizes , name="charge_sizes"),


    path("tiendas", views.stores , name="stores"),
    path("contacto", views.contact, name="contact"),
    path("pago", views.checkout, name="checkout"),

    path("cart", views.cart, name="cart"),
    path("filter-data",views.filter_data, name="filter"),
    path("search",views.search, name="search"),
    
    
    
    # path('cat/<int:cat_id>/',views.category_product_list,name='category-product-list'),

]
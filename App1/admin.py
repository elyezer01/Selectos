from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    # list_display = ("ref", "description", "price", "total_quantity", "available_colors")
    list_display = ("ref", "description", "price", "available_colors")

    # def total_quantity(self, obj):
    #     from django.db.models import Sum
    #     result = Variant.objects.filter(parent=obj).aggregate(Sum("quantity"))
    #     return result["quantity__sum"]

    def available_colors(self, obj):
        result = Variant.objects.filter(parent=obj).values("color").distinct()
        return [i['color'] for i in result]

class VariantAdmin(admin.ModelAdmin):
    list_display = ("parent", "color", "quantity")
    search_fields = ( "color" ,)

    def quantity(self, obj):
        from django.db.models import Sum
        result = Quantity.objects.filter(variant=obj).aggregate(Sum("quantity"))
        return result["quantity__sum"]

admin.site.register(product, ProductAdmin)
admin.site.register(Variant,VariantAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(store)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Quantity)
admin.site.register(Department)


# admin.site.unregister(Groups)

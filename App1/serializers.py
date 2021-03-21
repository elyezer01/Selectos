from rest_framework import serializers
from .models import *

class VariantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variant
		fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
	principal = VariantSerializer(read_only=True, many=True)
	class Meta:
		model = product
		fields = ['id','ref','description','price','category','img','principal']
		

class StoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = store
		fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
	product = VariantSerializer(read_only=True, many=True)
	class Meta:
		model = OrderItem
		fields = [        "id",
        "quantity",
        "date_added",
        "product",
        "order"	]
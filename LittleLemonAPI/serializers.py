from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class MenuItemSerializer(serializers.ModelSerializer):
    
    category_name = serializers.CharField(source='category.name',read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id','name','slug','description','price','category_name']
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Category, MenuItem, Cart, Order
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([AllowAny])
def MenuView(request):
    menuitems = MenuItem.objects.all()
    serializer = MenuItemSerializer(menuitems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def CategoryOrDetailView(request,slug):
    #check if slug is a category
    category = Category.objects.filter(slug=slug)

    if category.exists():
        category = category.first()
        menuitems = MenuItem.objects.filter(category=category)
        serializer = MenuItemSerializer(menuitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #check if slug is a menu item
    menuitem = MenuItem.objects.filter(slug=slug)
    
    if menuitem.exists():
        menuitem = menuitem.first()
        serializer = MenuItemSerializer(menuitem)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddToCartView(request):
    user = request.user
    data = request.data
    item = data['item']
    quantity = data['quantity']

    menuitem = get_object_or_404(MenuItem, id=item)
    cart_item = Cart.objects.create(
        user=user,
        item=menuitem,
        quantity=quantity
    )
    serializer = CartSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CartView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateOrderView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    order = Order.objects.create(user=user)
    order.items.add(*cart_items)
    return Response({'order_id':order.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def OrderDetailView(request,order_id):
    user = request.user
    order = Order.objects.filter(user=user,id=order_id)
    if order.exists():
        order = order.first()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def OrderListView(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def AllOrdersView(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



from django.urls import path, include

from . import views

urlpatterns = [
    path('menu/', views.MenuView, name='menu'),
    path('menu/<slug:slug>/', views.CategoryOrDetailView, name='category_or_detail'),
    path('add-to-cart/', views.AddToCartView, name='add_to_cart'),
    path('cart/', views.CartView, name='cart'),
    path('create-order/', views.CreateOrderView, name='create_order'),
    path('orders/', views.OrderListView, name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView, name='order_detail'),
    path('all-orders/', views.AllOrdersView, name='all_orders'),
]
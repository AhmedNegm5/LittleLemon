from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('user/',views.get_user,name='user'),
    path('update-user/',views.update_user,name='update_user'),
    path('delete-user/',views.delete_user,name='delete_user'),
]
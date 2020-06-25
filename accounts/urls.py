from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/', views.deleteOrder, name="delete_order"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),

]
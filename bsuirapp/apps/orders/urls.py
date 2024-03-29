from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('verify/<str:uid64>/<str:token>/', views.verify, name='verify_order'),
]
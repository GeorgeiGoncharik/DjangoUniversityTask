from . import views
from django.urls import path, include

app_name = 'products'
urlpatterns = [
    path('', views.products_list, name='index'),
    path('<slug:category_slug>/', views.products_list, name='index_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
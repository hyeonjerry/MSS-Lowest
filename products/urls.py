from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.productsList, name='productsList'),
    path('<product_id>/', views.productDetail, name='productDetail'),
]

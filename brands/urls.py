from django.urls import path

from brands import views

app_name = 'brands'

urlpatterns = [
    path('', views.brandsList, name='brandsList'),
    path('<brand_id>/', views.brandDetail, name='brandDetail'),
]

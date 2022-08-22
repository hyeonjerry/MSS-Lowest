from django.urls import path, include
from rest_framework.routers import DefaultRouter

from brands import views

app_name = 'brands'

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet, basename="brand")

urlpatterns = [
    path('', views.brandsList, name='brandsList'),
    path('api/', include(router.urls)),
    path('<brand_id>/', views.brandDetail, name='brandDetail'),
]

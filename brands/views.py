from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets

from brands.models import Brand
from brands.serializers import BrandSerializer


def brandsList(request):
    kw = request.GET.get('kw', '')
    page = request.GET.get('page', '1')
    if kw:
        brands = Brand.objects.filter(Q(ko_name__icontains=kw) | Q(
            en_name__icontains=kw)).distinct().order_by('en_name')
    else:
        brands = Brand.objects.order_by('en_name')
    paginator = Paginator(brands, 15)
    page_obj = paginator.get_page(page)
    context = {'page_objs': page_obj, 'page': page, 'kw': kw}
    return render(request, 'brands/list.html', context)


def brandDetail(request, brand_id):
    page = request.GET.get('page', '1')
    brand = Brand.objects.get(id=brand_id)
    products = brand.brand_product.all()
    products = Paginator(products, 15).get_page(page)
    context = {'brand': brand, 'page_objs': products, 'page': page}
    return render(request, 'brands/detail.html', context)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

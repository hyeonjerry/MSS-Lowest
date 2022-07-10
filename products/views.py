from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from products.models import Product


def productsList(request):
    kw = request.GET.get('kw', '')
    page = request.GET.get('page', '1')
    if kw:
        products = Product.objects.filter(
            Q(name__icontains=kw) | Q(brand__ko_name__icontains=kw) | Q(brand__en_name__icontains=kw)).distinct().order_by('updated_date')
    else:
        products = Product.objects.order_by('-updated_date')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(page)
    context = {'page_objs': page_obj, 'page': page, 'kw': kw}
    return render(request, 'products/products_list.html', context)


def productDetail(request, product_id):
    product = Product.objects.get(id=product_id)
    histories = product.product_producthistory.all().order_by('-created_date')
    context = {'product': product, 'histories': histories}
    return render(request, 'products/product_detail.html', context)

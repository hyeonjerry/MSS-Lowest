from django.shortcuts import render
from django.core.paginator import Paginator

from products.models import Product, ProductHistory


def productsList(request):
    page = request.GET.get('page', '1')
    products = Product.objects.order_by('-updated_date')
    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(page)
    context = {'page_objs': page_obj, 'page': page}
    return render(request, 'products/products_list.html', context)

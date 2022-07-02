from django.shortcuts import render
from django.core.paginator import Paginator

from brands.models import Brand


def brandsList(request):
    page = request.GET.get('page', '1')
    brands = Brand.objects.order_by('en_name')
    paginator = Paginator(brands, 15)
    page_obj = paginator.get_page(page)
    context = {'brands': page_obj, 'page': page}
    return render(request, 'brands/brands_list.html', context)

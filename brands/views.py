from django.shortcuts import render

from brands.models import Brand


def brandsList(request):
    brands = Brand.objects.order_by('en_name')
    return render(request, 'brands/brands_list.html', context)

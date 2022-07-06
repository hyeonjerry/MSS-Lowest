from brands.models import Brand
from bs4 import BeautifulSoup
import requests
import django
django.setup()


URL = 'https://www.musinsa.com/app/contents/brandshop'
headers = {'user-agent': 'Mozilla/5.0'}


def createBrands():
    req = requests.get(URL, headers=headers)
    brands = BeautifulSoup(req.text, 'html.parser').select(
        '#text_list > ul > li > dl')
    data_gen = ((brand.dt.a.text, (lambda x: x[:x.rfind(' ')])(
        brand.dd.a.text), brand.dt.a.get('href')) for brand in brands)
    new_brands = [Brand(en_name=en, ko_name=ko, url=url, suffix=url.split('/')[-1])
                  for en, ko, url in data_gen if not Brand.objects.filter(url=url)]
    if new_brands:
        Brand.objects.bulk_create(new_brands)

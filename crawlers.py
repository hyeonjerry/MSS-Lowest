from bs4 import BeautifulSoup
import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
import django
django.setup()

from brands.models import Brand

headers = {'user-agent': 'Mozilla/5.0'}


def crawl_brands():
    URL = 'https://www.musinsa.com/app/contents/brandshop'
    BRAND_SELECTOR = '#text_list > ul > li > dl'

    def parse_brand(brand):
        row = brand.select_one('dd > a').text.split()
        ko_name = ' '.join(row[:-1])
        is_verify = row[-1][1:-1] != '0'
        en_name = brand.select_one('dt > a').text
        url = brand.select_one('dt > a').get('href')
        return ko_name, en_name, url, is_verify

    with requests.get(URL, headers=headers) as req:
        brands = BeautifulSoup(req.text, 'html.parser').select(BRAND_SELECTOR)

    brands = [parse_brand(brand) for brand in brands]
    new_brands = [Brand(ko_name=ko, en_name=en, url=url)
                  for ko, en, url, is_verify in brands
                  if is_verify and not Brand.objects.filter(url=url)]
    Brand.objects.bulk_create(new_brands)

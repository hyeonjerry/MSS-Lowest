from pathlib import Path
BASE = Path(__file__).resolve().parent.parent.__str__()
import sys
sys.path.append(BASE)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from concurrent.futures import ThreadPoolExecutor, as_completed

from products.models import Product, ProductHistory
from brands.models import Brand

HEADERS = {'user-agent': 'Mozilla/5.0'}


def update_brand():
    URL = 'https://www.musinsa.com/app/contents/brandshop'
    BRAND_SELECTOR = '#text_list > ul > li > dl'
    KO_NAME_SELECTOR = 'dl > dd > a'
    EN_NAME_SELECTOR = 'dl > dt > a'
    brands = []  # [(ko, en, url), ...]

    def parse_brand(obj):
        ko_name = obj.select_one(KO_NAME_SELECTOR).text
        ko_name = ko_name[:ko_name.rfind(' ')]
        en_name = obj.select_one(EN_NAME_SELECTOR)
        en_name, url = en_name.text, en_name.get('href')
        return ko_name, en_name, url

    def get_brand_obj(brand):
        PRODUCT_SELECTOR = '#searchList > li'
        ko_name, en_name, url = brand

        with requests.get(url, headers=HEADERS) as request:
            source = BeautifulSoup(request.text, 'html.parser')
        product_cnt = len(source.select(PRODUCT_SELECTOR))

        if product_cnt == 0:
            return None
        return Brand(ko_name=ko_name, en_name=en_name, url=url)

    with requests.get(URL, headers=HEADERS) as request:
        source = BeautifulSoup(request.text, 'html.parser')

    # [ (ko, en, url), (ko, en, url), ... ]
    brands = [items for brand in source.select(BRAND_SELECTOR)
              if ((items := parse_brand(brand)) and
                  not Brand.objects.filter(url=items[2]))]

    with ThreadPoolExecutor(max_workers=os.cpu_count()*2) as executor:
        futures = [executor.submit(get_brand_obj, brand) for brand in brands]

    # [ Brand(None), Brand(None), ... ]
    brands = [result for future in as_completed(futures)
              if (result := future.result())]
    Brand.objects.bulk_create(brands)


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(update_brand, 'cron', hour='5',
                  minute='0', id='update_brand')
    sched.start()

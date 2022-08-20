from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import requests
import re

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
import django
django.setup()

from products.models import Product, ProductHistory
from brands.models import Brand

HEADERS = {'user-agent': 'Mozilla/5.0'}
brands = Brand.objects.all()
products = Product.objects.all()
histories = ProductHistory.objects.all()


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

    with requests.get(URL, headers=HEADERS) as req:
        brands_ = BeautifulSoup(req.text, 'html.parser').select(BRAND_SELECTOR)

    brands_ = [parse_brand(brand) for brand in brands_]
    new_brands = [Brand(ko_name=ko, en_name=en, url=url)
                  for ko, en, url, is_verify in brands_
                  if is_verify and not brands.filter(url=url)]
    brands.bulk_create(new_brands)


def crawl_products_each_brand():
    def parse_price(price):
        return int(''.join(re.findall(r'\d+', price)))

    def parse_product(product, brand):
        NAME_SELECTOR = 'div.article_info > p.list_info > a'
        IMAGE_SELECTOR = 'div.list_img > a > img'
        PRICE_SELECTOR = 'div.article_info > p.price'

        name = product.select_one(NAME_SELECTOR).get('title')
        image = 'https:' + \
                product.select_one(IMAGE_SELECTOR).get('data-original')
        price = product.select_one(PRICE_SELECTOR).text.split()
        retail_price = parse_price(price[0])
        last_price = parse_price(price[-1])
        url = 'https:' + product.select_one(NAME_SELECTOR).get('href')
        id_ = int(url[url.rfind('/')+1:])

        return id_, name, brand, retail_price, last_price, image, url

    def crawl_products(brand):
        URL = brand.url + '?page=%d'
        PAGE_SELECTOR = '#product_list > div.section_product_list > div:nth-child(1) > div.boxed-list-wrapper > div.thumbType_box.box > span.pagingNumber > span.totalPagingNum'
        PRODUCT_SELECTOR = '#searchList > li > div.li_inner'

        req = requests.get(brand.url, headers=HEADERS)
        soup = BeautifulSoup(req.text, 'html.parser')
        total_page = int(soup.select_one(PAGE_SELECTOR).text)

        page = 2
        products_ = []
        while True:
            data = soup.select(PRODUCT_SELECTOR)
            products_.extend([parse_product(product, brand)
                             for product in data])

            if page > total_page:
                break
            req = requests.get(URL % page, headers=HEADERS)
            soup = BeautifulSoup(req.text, 'html.parser')
            page += 1

        return products_

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(crawl_products, brand) for brand in brands]

    for future in as_completed(futures):
        products_ = future.result()
        new_products = [Product(id=id_, name=name, brand=brand, retail_price=retail_price, image=image, url=url)
                        for id_, name, brand, retail_price, last_price, image, url in products_
                        if not products.filter(pk=id_)]
        products.bulk_create(new_products)
        new_histories = [ProductHistory(product=products.get(pk=product[0]), price=product[4])
                         for product in products_]
        histories.bulk_create(new_histories)

        update_products = []
        for history in new_histories:
            product = history.product
            if not product.last_price:
                product.last_price = history
                product.lowest_price = history
                product.highest_price = history
            else:
                product.last_price = history
                if product.lowest_price.price > history.price:
                    product.lowest_price = history
                if product.highest_price.price < history.price:
                    product.highest_price = history
            update_products.append(product)
        products.bulk_update(
            update_products, ['last_price', 'lowest_price', 'highest_price'])


crawl_brands()
crawl_products_each_brand()

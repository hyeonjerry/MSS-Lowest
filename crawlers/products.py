import re
import requests
from bs4 import BeautifulSoup

from products.models import Category, Product, ProductHistory
from brands.models import Brand

headers = {'user-agent': 'Mozilla/5.0'}


def getLargeCategories():
    URL = 'https://www.musinsa.com/ranking/best'
    url_prefix = 'https://www.musinsa.com/category/'
    categories_selector = '#goodsRankForm > div.clear > div:nth-child(16) > dl > dd > ul > li > a'

    req = requests.get(URL, headers=headers)
    categories = BeautifulSoup(
        req.text, 'html.parser').select(categories_selector)

    names = [category.text for category in categories]
    urls = [url_prefix + re.search(r'\d+', category.get('href')).group()
            for category in categories]

    return names, urls


def getMediumCategories(url):
    url_prefix = 'https://www.musinsa.com/category/'
    categories_selector = '#category_2depth_list > dl > dd > ul > li > a'

    req = requests.get(url, headers=headers)
    categories = BeautifulSoup(
        req.text, 'html.parser').select(categories_selector)

    names = [category.get('data-value') for category in categories]
    urls = [url_prefix + category.get('data-code') for category in categories]

    return names, urls


def createCategories():
    names, urls = getLargeCategories()
    new_categories = [Category(name=name, url=url) for name, url in zip(
        names, urls) if not Category.objects.filter(name=name)]
    if new_categories:
        Category.objects.bulk_create(new_categories)

    for name, url in zip(names, urls):
        m_names, m_urls = getMediumCategories(url)
        l_category = Category.objects.get(name=name)
        new_categories = [Category(parent=l_category, name=m_name, url=m_url) for m_name, m_url in zip(
            m_names, m_urls) if not Category.objects.filter(name=m_name)]
        if new_categories:
            Category.objects.bulk_create(new_categories)


def getProducts(url):
    full_url = url + '?page=%d'
    page_selector = '#product_list > div.section_product_list > div:nth-child(1) > div.boxed-list-wrapper > div.thumbType_box.box > span.pagingNumber > span.totalPagingNum'
    names_selector = '#searchList > li > div.li_inner > div.article_info > p.list_info > a'
    prices_selector = '#searchList > li > div.li_inner > div.article_info > p.price'
    thumbnails_selector = '#searchList > li > div.li_inner > div.list_img > a > img'
    urls_selector = '#searchList > li > div.li_inner > div.article_info > p.list_info > a'
    re_num = re.compile('\d+')
    page = 2

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    total_page = int(soup.select_one(page_selector).text)

    names = []
    req_prices = []
    now_prices = []
    thumbnails = []
    urls = []
    while True:
        names.extend([item.get('title')
                     for item in soup.select(names_selector)])
        req_prices.extend([int(''.join(re_num.findall(item.text.split()[0])))
                          for item in soup.select(prices_selector)])
        now_prices.extend([int(''.join(re_num.findall(item.text.split()[-1])))
                          for item in soup.select(prices_selector)])
        thumbnails.extend(['https:' + item.get('data-original')
                          for item in soup.select(thumbnails_selector)])
        urls.extend(['http:' + item.get('href')
                    for item in soup.select(urls_selector)])

        if page > total_page:
            break
        req = requests.get(full_url % page, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        page += 1

    return names, req_prices, now_prices, thumbnails, urls


def createProductsByBrand():
    brands = Brand.objects.all()

    for brand in brands:
        try:
            names, req_prices, now_prices, thumbnails, urls = getProducts(
                brand.url)
        except:
            continue

        new_products = [Product(name=name, brand=brand, requested_price=req_price, thumbnail=thumbnail, url=url)
                        for name, req_price, thumbnail, url in zip(names, req_prices, thumbnails, urls) if not Product.objects.filter(url=url)]
        Product.objects.bulk_create(new_products)

        products = [Product.objects.get(url=url) for url in urls]
        new_histories = [ProductHistory(product=product, price=price)
                         for product, price in zip(products, now_prices)]
        ProductHistory.objects.bulk_create(new_histories)

        for product in products:
            price = product.product_producthistory.last()
            product.last_price = price
            if product.lowest_price is None or product.lowest_price.price > price.price:
                product.lowest_price = price
            if product.highest_price is None or product.highest_price.price < price.price:
                product.highest_price = price

        Product.objects.bulk_update(
            products, ['last_price', 'lowest_price', 'highest_price'])

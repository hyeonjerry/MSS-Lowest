import re
import requests
from bs4 import BeautifulSoup

from products.models import Category

headers = {'user-agent': 'Mozilla/5.0'}


# 대분류 수집
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

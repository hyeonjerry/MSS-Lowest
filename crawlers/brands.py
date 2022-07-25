from concurrent.futures import ThreadPoolExecutor, as_completed
from brands.models import Brand
from bs4 import BeautifulSoup
import requests
import re

URL = 'https://www.musinsa.com/app/contents/brandshop'
headers = {'user-agent': 'Mozilla/5.0'}
re_num = re.compile('\d+')


def createBrands():
    with requests.get(URL, headers=headers) as req:
        brands = BeautifulSoup(req.text, 'html.parser').select(
            '#text_list > ul > li > dl')

    data_gen = ((brand.dt.a.text, *_splitKoCnt(brand.dd.a.text),
                brand.dt.a.get('href')) for brand in brands)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(_checkVerification, en, ko, url) for en, ko,
                   cnt, url in data_gen if cnt > 0 and not Brand.objects.filter(url=url)]
    new_brands = [Brand(en_name=result[0], ko_name=result[1], url=result[2])
                  for future in as_completed(futures) if (result := future.result())]

    if new_brands:
        Brand.objects.bulk_create(new_brands)


def _splitKoCnt(x):
    return x[:x.rfind(' ')], int(''.join(re_num.findall(x[x.rfind('(')+1:-1])))


def _checkVerification(en, ko, url):
    with requests.get(url, headers=headers) as req:
        soup = BeautifulSoup(req.text, 'html.parser')
    if soup.select('#searchList'):
        return en, ko, url
    else:
        return False

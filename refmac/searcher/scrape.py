from .products import *

from bs4 import BeautifulSoup
from typing import List

import requests


BASE_URL = 'https://www.apple.com'

PRODUCT_LISTING_PAGES = {
    Products.MBP: '/shop/browse/home/specialdeals/mac/macbook_pro',
    Products.MBP_13: '/shop/browse/home/specialdeals/mac/macbook_pro/13',
    Products.MBP_15: '/shop/browse/home/specialdeals/mac/macbook_pro/15',
}


class Specs:
    def __init__(self, released: str, screen: str, memory: str, ssd: str, touch_bar: bool):
        self.released = released
        self.screen = screen
        self.memory = memory
        self.ssd = ssd
        self.touch_bar = touch_bar
        for k, v in vars(self).items():
            if v is None:
                raise RuntimeError(f"No value supplied to Specs for field: {k}")

    def __repr__(self):
        return repr(vars(self))


class Product:
    def __init__(self, object_id: str, name: str, price: str, url: str, specs: Specs):
        self.object_id = object_id
        self.name = name
        self.price = price
        self.url = url
        self.specs = specs
        for k, v in vars(self).items():
            if v is None:
                raise RuntimeError("No value supplied to Product for field: {k}")

    def __repr__(self):
        return self.name


def get_current_listings_for_product(product: Products) -> List[Product]:
    url = BASE_URL + PRODUCT_LISTING_PAGES[product]
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html5lib")
    refurb_list = soup.find(**{'class': 'refurb-list'})
    box = refurb_list.find(**{'class': 'box-content'})
    tables = box.findAll('table')
    return list(map(process_listing_table, tables))


def process_listing_table(table: BeautifulSoup) -> Product:
    product = table.find(**{'class': 'product'})
    if product is None:
        raise RuntimeError("False table found.")
    raw_specs = product.find(**{'class': 'specs'})
    if raw_specs is None:
        raise RuntimeError("No specs found.")
    title = raw_specs.h3
    object_id = title.a['data-s-object-id']
    name = title.a.text.strip()
    url = BASE_URL + title.a['href']
    try:
        specs = process_specs(simplify_specs(raw_specs.text))
    except RuntimeError:
        print("Could not process specs for product:")
        print("  " + name)
        print("  " + url)
        raise
    raw_price = product.find(**{'itemprop': 'price'})
    if raw_price is None:
        raise RuntimeError("No price found.")
    price = raw_price.text.strip()
    return Product(object_id=object_id, name=name, price=price, url=url, specs=specs)


def simplify_specs(text: str) -> List[str]:
    return list(filter(lambda x: bool(x), map(str.strip, text.split('\n'))))


def process_specs(specs: List[str]) -> Specs:
    released = find_line(specs, 'released')
    screen = find_line(specs, 'resolution')
    memory = find_line(specs, 'onboard memory')
    ssd = find_line(specs, 'PCIe-based')
    touch_bar = has_reference(specs, 'Touch Bar')
    return Specs(released=released, screen=screen, memory=memory, ssd=ssd, touch_bar=touch_bar)


def find_line(lines: List[str], keyword: str) -> str:
    result = None
    for line in lines:
        if keyword in line:
            if result is not None:
                raise RuntimeError(f"Too many lines with keyword: {keyword}")
            result = line
    return result


def has_reference(lines: List[str], keyword: str) -> bool:
    for line in lines:
        if keyword in line:
            return True
    return False

from bs4 import BeautifulSoup
from typing import List

import requests


PRODUCT_CATEGORIES = {
    'mbp-13': 'https://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro/13',
}


class Specs:
    def __init__(self, release: str, screen: str, memory: str, ssd: str, camera: str, graphics: str, touch_bar: bool):
        self.release = release
        self.screen = screen
        self.memory = memory
        self.ssd = ssd
        self.camera = camera
        self.graphics = graphics
        self.touch_bar = touch_bar

    def __repr__(self):
        return repr(vars(self))


class Product:
    def __init__(self, name: str, price: str, url: str, specs: Specs):
        self.name = name
        self.price = price
        self.url = url
        self.specs = specs

    def __repr__(self):
        return self.name


def get_current_listings(product: str) -> List[Product]:
    url = PRODUCT_CATEGORIES[product]
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
    url = title.a['href']
    name = title.a.text.strip()
    specs = process_specs(simplify_specs(raw_specs.text))
    raw_price = product.find(**{'itemprop': 'price'})
    if raw_price is None:
        raise RuntimeError("No price found.")
    price = raw_price.text.strip()
    return Product(name=name, price=price, url=url, specs=specs)


def simplify_specs(text: str) -> List[str]:
    return list(filter(lambda x: bool(x), map(str.strip, text.split('\n'))))


def process_specs(specs: List[str]) -> Specs:
    release = find_line(specs, 'released')
    screen = find_line(specs, 'resolution')
    memory = find_line(specs, 'memory')
    ssd = find_line(specs, 'SSD')
    camera = find_line(specs, 'Camera')
    graphics = find_line(specs, 'Graphics')
    touch_bar = has_reference(specs, 'Touch Bar')
    return Specs(release=release, screen=screen, memory=memory, ssd=ssd, camera=camera, graphics=graphics,
                 touch_bar=touch_bar)


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

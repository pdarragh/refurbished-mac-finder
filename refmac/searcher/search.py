from .producttype import *
from .scrape import Product, get_current_listings_for_product

from functools import partial
from typing import Callable, List


Specification = Callable[[Product], bool]


def search_for_products_matching_specifications(product_type: ProductType, specifications: List[Specification]
                                                ) -> List[Product]:
    listings = filter(lambda l: l is not None, get_current_listings_for_product(product_type))
    for specification in specifications:
        listings = filter(specification, listings)
    return list(listings)


def matches_name(name: str, product: Product) -> bool:
    return name in product.name


def below_price(price: str, product: Product) -> bool:
    max_price = process_price(price)
    item_price = process_price(product.price)
    return item_price <= max_price


def matches_release_date(date: str, product: Product) -> bool:
    return date in product.specs.released


def matches_screen(screen: str, product: Product) -> bool:
    return screen in product.specs.screen


def matches_memory(memory: str, product: Product) -> bool:
    return memory in product.specs.memory


def matches_ssd(ssd: str, product: Product) -> bool:
    return ssd in product.specs.ssd


def has_touch_bar(want: str, product: Product) -> bool:
    return bool(want) == product.specs.touch_bar


def process_price(price: str) -> float:
    price = price.strip('$').replace(',', '')
    parts = price.split('.')
    dollars = int(parts[0])
    if len(parts) > 1:
        cents = int(parts[1])
    else:
        cents = 0
    return dollars + (cents / 100)


SPECIFICATIONS = {
    'name': matches_name,
    'price': below_price,
    'release_date': matches_release_date,
    'screen': matches_screen,
    'memory': matches_memory,
    'ssd': matches_ssd,
    'touch_bar': has_touch_bar,
}


def build_specifications(**kwargs) -> List[Specification]:
    specifications: List[Specification] = []
    for key, val in kwargs.items():
        specifications.append(partial(SPECIFICATIONS[key], val))
    return specifications

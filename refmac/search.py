from .products import *
from .scrape import Product, get_current_listings_for_product

from typing import Callable, List


def search_for_products_matching_specifications(product: Products, specifications: List[Callable[[Product], bool]]
                                                ) -> List[Product]:
    listings = get_current_listings_for_product(product)
    for specification in specifications:
        listings = filter(specification, listings)
    return list(listings)


def below_price(price: str, product: Product) -> bool:
    price = float(price[1:])
    return float(product.price[1:]) < price


def matches_release_date(date: str, product: Product) -> bool:
    return date in product.specs.released


def matches_screen(screen: str, product: Product) -> bool:
    return screen in product.specs.screen


def matches_memory(memory: str, product: Product) -> bool:
    return memory in product.specs.memory


def matches_ssd(ssd: str, product: Product) -> bool:
    return ssd in product.specs.ssd


def matches_camera(camera: str, product: Product) -> bool:
    return camera in product.specs.camera


def matches_graphics(graphics: str, product: Product) -> bool:
    return graphics in product.specs.graphics


def has_touch_bar(product: Product) -> bool:
    return product.specs.touch_bar

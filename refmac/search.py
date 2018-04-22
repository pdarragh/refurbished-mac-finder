from .products import *
from .scrape import Product, get_current_listings_for_product

from typing import Callable, List


def search_for_products_matching_specifications(product: Products, specifications: List[Callable[[Product], bool]]
                                                ) -> List[Product]:
    listings = get_current_listings_for_product(product)
    for specification in specifications:
        listings = filter(specification, listings)
    return list(listings)

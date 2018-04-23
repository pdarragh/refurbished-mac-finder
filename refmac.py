#!/usr/bin/env python3
from refmac.searcher import *

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('product_type', metavar='product-type', choices=[t for t in ProductType], type=lambda s: getattr(ProductType, s))
    parser.add_argument('--specs', type=json.loads, default={})
    args = parser.parse_args()

    print(f"Looking for products of type {args.product_type.name} with specifications: {args.specs}")

    products = search_for_products_matching_specifications(args.product_type, build_specifications(**args.specs))
    for product in products:
        print(product)
        print()

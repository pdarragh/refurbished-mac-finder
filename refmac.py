#!/usr/bin/env python3
from refmac.searcher import *

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('product_type', metavar='product-type', choices=[t for t in ProductType], type=lambda s: getattr(ProductType, s))
    parser.add_argument('--auth-file', type=argparse.FileType('r'))
    parser.add_argument('--twilio-sid')
    parser.add_argument('--twilio-token')
    parser.add_argument('--specs', type=json.loads, default={})
    args = parser.parse_args()

    twilio_account_sid = None
    twilio_auth_token = None

    if args.auth_file is not None:
        auth = json.load(args.auth_file)
        twilio_account_sid = auth['account_sid']
        twilio_auth_token = auth['auth_token']

    if args.twilio_sid is not None:
        twilio_account_sid = args.twilio_sid

    if args.twilio_token is not None:
        twilio_auth_token = args.twilio_token

    if twilio_account_sid is None:
        raise RuntimeError("No Twilio account SID given!")

    if twilio_auth_token is None:
        raise RuntimeError("No Twilio auth token given!")

    print(f"Looking for products of type {args.product_type.name} with specifications: {args.specs}")

    products = search_for_products_matching_specifications(args.product_type, build_specifications(**args.specs))
    for product in products:
        print(product)
        print()

#!/usr/bin/env python3
from refmac import *

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('product_type', metavar='product-type', choices=[t for t in ProductType], type=lambda s: getattr(ProductType, s))
    parser.add_argument('--twilio-file', type=argparse.FileType('r'), default='twilio_conf.json')
    parser.add_argument('--twilio-sid')
    parser.add_argument('--twilio-token')
    parser.add_argument('--send-from')
    parser.add_argument('--send-to')
    parser.add_argument('--specs', type=json.loads, default={})
    args = parser.parse_args()

    twilio_account_sid = None
    twilio_auth_token = None
    send_from = None
    send_to = None

    if args.twilio_file is not None:
        conf = json.load(args.twilio_file)
        twilio_account_sid = conf['account_sid']
        twilio_auth_token = conf['auth_token']
        send_from = conf['send_from']
        send_to = conf['send_to']

    if args.twilio_sid is not None:
        twilio_account_sid = args.twilio_sid

    if args.twilio_token is not None:
        twilio_auth_token = args.twilio_token

    if args.send_from is not None:
        send_from = args.send_from

    if args.send_to is not None:
        send_to = [args.send_to]

    if twilio_account_sid is None:
        raise RuntimeError("No Twilio account SID given!")

    if twilio_auth_token is None:
        raise RuntimeError("No Twilio auth token given!")

    if send_from is None:
        raise RuntimeError("No send-from number given!")

    if send_to is None:
        raise RuntimeError("No send-to number given!")

    print(f"Looking for products of type {args.product_type.name} with specifications: {args.specs}")

    find_and_notify(args.product_type, args.specs, twilio_account_sid, twilio_auth_token, send_from, send_to)

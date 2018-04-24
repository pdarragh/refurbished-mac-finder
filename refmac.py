#!/usr/bin/env python3
from refmac import *

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('product_type', metavar='product-type', choices=[t for t in ProductType],
                        type=lambda s: getattr(ProductType, s),
                        help="The product space to search through. See documentation.")
    parser.add_argument('--twilio-file', type=argparse.FileType('r'), default='twilio_conf.json',
                        help="A JSON file providing Twilio configuration. See documentation.")
    parser.add_argument('--twilio-sid',
                        help="Your Twilio account SID.")
    parser.add_argument('--twilio-token',
                        help="Your Twilio account auth token.")
    parser.add_argument('--send-from',
                        help="The phone number to send results from. (Your Twilio phone number.)")
    parser.add_argument('--send-to',
                        help="The phone number to send results to.")
    parser.add_argument('--emergency-contact',
                        help="A phone number to contact if an exception occurs. Only compatible with --retry.")
    parser.add_argument('--specs', type=json.loads, default={},
                        help="The specifications to search for. See documentation.")
    parser.add_argument('--retry', type=int, default=0,
                        help="Retry the search every RETRY minutes. A value of 0 means no retry will occur.")
    parser.add_argument('--verbose', action='store_true',
                        help="Output information about matches found to stdout.")
    parser.add_argument('--no-notify', action='store_true',
                        help="Do not send text notifications.")
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

    if not args.no_notify and twilio_account_sid is None:
        raise RuntimeError("No Twilio account SID given!")

    if not args.no_notify and twilio_auth_token is None:
        raise RuntimeError("No Twilio auth token given!")

    if not args.no_notify and send_from is None:
        raise RuntimeError("No send-from number given!")

    if not args.no_notify and send_to is None:
        raise RuntimeError("No send-to number given!")

    print(f"Looking for products of type {args.product_type.name} with specifications: {args.specs}")

    find_and_notify(args.product_type, args.specs, twilio_account_sid, twilio_auth_token, send_from, send_to,
                    args.retry, args.verbose, args.no_notify, args.emergency_contact)

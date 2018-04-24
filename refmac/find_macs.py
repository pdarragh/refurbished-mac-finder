from .searcher import *
from .notify import *

from typing import Dict, List


def find_and_notify(product_type: ProductType, specs: Dict[str, str], account_sid: str, auth_token: str, send_from: str,
                    send_to: List[str], verbose: bool, no_notify: bool):
    specifications = build_specifications(**specs)
    matches = search_for_products_matching_specifications(product_type, specifications)
    if verbose:
        print("Found the following products matching given specifications:")
        for match in matches:
            print()
            print(match)
        print()
    if not no_notify:
        for number in send_to:
            if verbose:
                print("Notifying " + number)
            notifier = Notifier(account_sid, auth_token, send_from)
            for match in matches:
                lines = [
                    match.name,
                    match.price,
                    match.url
                ]
                message = '\n'.join(lines)
                notifier.send_message(message, number)

from .searcher import *
from .notify import *

from typing import Dict, List


def find_and_notify(product_type: ProductType, specs: Dict[str, str], account_sid: str, auth_token: str, send_from: str,
                    send_to: List[str]):
    specifications = build_specifications(**specs)
    matches = search_for_products_matching_specifications(product_type, specifications)
    for number in send_to:
        notifier = Notifier(account_sid, auth_token, send_from)
        for match in matches:
            lines = [
                match.name,
                match.price,
                match.url
            ]
            message = '\n'.join(lines)
            notifier.send_message(message, number)

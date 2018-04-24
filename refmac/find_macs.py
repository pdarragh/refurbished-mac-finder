from .searcher import *
from .notify import *

from functools import partial
from sys import stderr
from time import sleep
from typing import Dict, List, Optional


def find_and_notify(product_type: ProductType, specs: Dict[str, str], account_sid: str, auth_token: str, send_from: str,
                    send_to: List[str], retry: int, verbose: bool, no_notify: bool, emergency_contact: Optional[str]):
    specifications = build_specifications(**specs)
    notifier = Notifier(account_sid, auth_token, send_from)
    find = partial(_find_and_notify, product_type, specifications, notifier, send_to, verbose, no_notify)
    # Run once no matter what.
    find()
    # If needed, do a loop.
    count = retry
    while retry:
        print(f"{count} minutes until next check...")
        sleep(60)
        count -= 1
        if count <= 0:
            try:
                find()
            except Exception as e:
                if emergency_contact is not None:
                    # Print the error message and notify the emergency contact.
                    print(e, file=stderr)
                    notifier.send_message("Exception occurred.", emergency_contact)
                else:
                    # No emergency contact, so halt execution.
                    raise e
            # Mr Gaeta, restart the clock.
            count = retry


def _find_and_notify(product_type: ProductType, specifications: List[Specification], notifier: Notifier,
                     send_to: List[str], verbose: bool, no_notify: bool):
    matches = search_for_products_matching_specifications(product_type, specifications)
    if not matches:
        if verbose:
            print("No matches found.")
        return
    if no_notify or verbose:
        print("Found the following products matching given specifications:")
        for match in matches:
            print()
            print(match)
        print()
    if not no_notify:
        for number in send_to:
            for match in matches:
                lines = [
                    match.name,
                    match.price,
                    match.url
                ]
                message = '\n'.join(lines)
                if verbose:
                    print("Notifying " + number + " of match " + match.name)
                notifier.send_message(message, number)


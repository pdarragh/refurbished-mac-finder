# Refurbished Mac Finder

A tool to help you keep an eye on Apple's [refurbished MacBook Pros](https://www.apple.com/shop/browse/home/specialdeals/mac/macbook_pro).

## Prerequisites

This project was built using Python 3.6 features, and it relies on BeautifulSoup 4 (using html5lib) and Twilio's API.
Required libraries can be installed via `pip3 install -r requirements.txt`.

## Usage

`refmac.py` takes one positional argument and a number of optional parameters.

The positional argument describes which products to search. These are the currently supported options:

| Parameter | Product Type     |
|-----------|------------------|
| `MBP`     | All MacBook Pros |
| `MBP_13`  | 13" MacBook Pros |
| `MBP_15`  | 15" MacBook Pros |

The optional parameters are:

| Option                | Effect |
|-----------------------|--------|
| `--help`              | Show a help message and quit. |
| `--twilio-file`       | Provide a configuration file (detailed below) for Twilio authentication/notification. |
| `--twilio-sid`        | Provide a Twilio account SID manually. |
| `--twilio-token`      | Provide a Twilio account auth token. |
| `--send-from`         | Manually specify a number to send texts from (should be your Twilio number). |
| `--send-to`           | Manually specify a number to send texts to. |
| `--specs`             | A JSON dictionary representing the specifications to search for (detailed below). |
| `--retry`             | A number of minutes to wait before automatically repeating the search indefinitely. |
| `--emergency-contact` | A number to send texts to if an error occurs while retrying (only has effect with `--retry`). |
| `--verbose`           | Print out search information to stdout. |
| `--no-notify`         | Do not send messages via Twilio. |

## Twilio Configuration File

You may provide a JSON file to use as configuration. The accepted structure is:

```json
{
  "account_sid": "<YOUR_TWILIO_ACCOUNT_SID_HERE>",
  "auth_token": "<YOUR_TWILIO_ACCOUNT_AUTH_TOKEN_HERE>",
  "send_from": "<YOUR_TWILIO_PHONE_NUMBER_HERE>",
  "send_to": [
    "5558675309",
    "5551234567"
  ]
}
```

The `send_to` field must be structured as a list, even if you have only one number. You may specify as many numbers as
you like, and they will all be notified by text when a match is found.

## Specifications

There are various options you can specify to search over. Currently supported are:

- name
- price
- release date
- screen
- memory
- ssd
- touch_bar

All values should be given as strings (and `touch_bar` will only work with arguments `True` or `False` ). The search is
very simple: `refmac` will merely attempt to find the given string in the relevant parameter's text. So if you want to
find a Mac with 16GB of RAM, you would specify `"memory": "16GB"`. There is currently no support for multiple different
arguments being passed (i.e. you cannot specify to look for either 16GB or 8GB of RAM).

`price` works slightly differently. Instead of matching an exact price, `refmac` will return any results that have a
price *less than or equal to* the specified price. The `price` parameter accepts prices in any of the following forms:

- `"$1,099.00"`
- `"$1099.00"`
- `"1,099.00"`
- `"1099.00"`
- `"1099"`

## Further Development

Additional product types should be supported. However, this may require reworking the `Product` and `Specs` classes to
be able to handle information from more varied product lines. (It would also require revising the functions in
`refmac/searcher/search.py`.)

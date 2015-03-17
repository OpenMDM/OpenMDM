import json
from django.core import serializers
import re


def format_object_to_plist(obj):
    """
    Formats all keys from a python-like dictionary to plist-like variable
    """
    dictionary = json.loads(serializers.serialize('json', [obj]))
    dictionary = dictionary[0]['fields']
    return {re.sub(r"_([a-z0-9])", underscore_to_camel_case, str(key)):  value for key, value in dictionary.items()}


def underscore_to_camel_case(match):
    """
    Transforms python-like variable (with _ separator) to plist-like variable (camel-cased)
    """
    return match.group(1).upper()

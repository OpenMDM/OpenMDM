import json
from django.core import serializers
import re


def format_object_to_plist(obj):
    """
    Formats all keys from a python-like dictionary to plist-like variable
    """
    dictionary = json.loads(serializers.serialize('json', [obj]))
    dictionary = dictionary[0]['fields']
    result = {}
    for key, value in dictionary.items():
        # The goal here is to transform variable looking like this
        #   this_is_1_random_var
        # to this
        #   ThisIs1RandomVar
        # So next line replaces ever _x with X
        key = re.sub(r"_([a-z0-9])", underscore_to_camel_case, str(key))
        # And this lines replaces the first letter with it's upper version
        key = key[:1].capitalize() + key[1:]
        result[key] = value
    return result


def underscore_to_camel_case(match):
    """
    Transforms python-like variable (with _ separator) to plist-like variable (camel-cased)
    """
    return match.group(1).upper()

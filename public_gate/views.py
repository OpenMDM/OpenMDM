import json
import re
from plistlib import dumps

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from public_gate.models import PropertyList, EmailAccount, Restrictions


def home(request):
    d = {}
    return render(request, 'home.html', d)


def about(request):
    d = {}
    return render(request, 'about.html', d)


def contact(request):
    d = {}
    return render(request, 'contact.html', d)


def property_list(request, plist_id):
    plist = PropertyList.objects.filter(id=plist_id)
    if 0 == len(plist):
        result = {"error": "This property list does not exist."}
        return render(request, 'property_list.html', dict(content=dumps(result)), content_type="application/xml")
    result = format_object_to_plist(plist)
    result['payloadContent'] = []
    # TODO Make this part generic. We don't want to add some lines when we add a model.
    email_property = EmailAccount.objects.filter(property_list_id=plist_id)
    if 0 != len(email_property):
        email_property = format_object_to_plist(email_property)
        result['payloadContent'].append(email_property)
    restriction_property = Restrictions.objects.filter(property_list_id=plist_id)
    if 0 != len(restriction_property):
        restriction_property = format_object_to_plist(restriction_property)
        result['payloadContent'].append(restriction_property)
    return render(request, 'property_list.html', dict(content=dumps(result)), content_type="application/xml")


def site_login(request):
    if request.method == "POST":
        user_login = request.POST['login']
        user_password = request.POST['password']
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            # User.objects.create_user(user_login, '', user_password).save()
            return render(request, 'home.html', {"error_message": "Wrong login/password combination"})
    return render(request, 'home.html', {"error_message": "One or more fields are empty"})


def site_logout(request):
    logout(request)
    return render(request, 'home.html')


def format_object_to_plist(obj):
    """
    Formats all keys from a python-like dictionary to plist-like variable
    """
    dictionary = json.loads(serializers.serialize('json', obj))
    dictionary = dictionary[0]['fields']
    return {re.sub(r"_([a-z0-9])", underscore_to_camel_case, str(key)):  value for key, value in dictionary.items()}


def underscore_to_camel_case(match):
    """
    Transforms python-like variable (with _ separator) to plist-like variable (camel-cased)
    """
    return match.group(1).upper()
import json
import re
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from public_gate.models import PropertyList, PropertyListForm, UserForm


def home(request):
    """
    Displays home page
    :param request:
    :return render:
    """
    d = {}
    return render(request, 'public_gate/home.html', d)


def about(request):
    """
    Displays about page
    :param request:
    :return render:
    """
    d = {}
    return render(request, 'public_gate/about.html', d)


def contact(request):
    """
    Displays contact page
    :param request:
    :return render:
    """
    d = {}
    return render(request, 'public_gate/contact.html', d)


########################################################################
#                                                                      #
#                       Authentication Views
#                                                                      #
########################################################################


def site_login(request):
    """
    Logs in current user
    :param request:
    :return render:
    """
    if request.method == "POST":
        user_login = request.POST['login']
        user_password = request.POST['password']
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('public_gate:home'))
        else:
            # User.objects.create_user(user_login, '', user_password).save()
            return render(request, 'public_gate/home.html', {"error_message": "Wrong login/password combination"})
    return render(request, 'public_gate/home.html', {"error_message": "One or more fields are empty"})


def site_logout(request):
    """
    Logs out current user
    :param request:
    :return render:
    """
    logout(request)
    return HttpResponseRedirect(reverse('public_gate:home'))


########################################################################
#                                                                      #
#                       Property List Views
#                                                                      #
########################################################################


def property_lists(request):
    """
    Fetches all property lists
    From: property_list/
    :param request: 
    :return render:
    """
    property_lists = PropertyList.objects.order_by('id')
    context = {'property_lists': property_lists}
    return render(request, 'public_gate/property_lists.html', context)


def property_lists_for_user(request, user_id):
    """
    Fetches plists for specific user
    From: user/<user_id>/property_list/
    :param request:
    :param user_id:
    :return render:
    """
    try:
        plist = PropertyList.objects.get(user_id=user_id)
    except PropertyList.DoesNotExist:
        return HttpResponse(status=404)
    return render(request, 'public_gate/property_lists.html', dict(plist=plist))


def property_list_detail(request, plist_id):
    """
    Fetches one plist
    From: property_list/<plist_id>/
    :param request: 
    :param plist_id: 
    :return render:
    """
    try:
        plist = PropertyList.objects.get(id=plist_id)
        dependencies = plist.get_dependent_properties()
    except PropertyList.DoesNotExist:
        return HttpResponse(status=404)
    plist_python = serializers.serialize("python", [plist])
    dependencies_json = serializers.serialize("python", dependencies)
    return render(request, 'public_gate/property_list_detail.html', dict(plist=plist,
                                                                         dependencies=dependencies,
                                                                         plist_python=plist_python,
                                                                         dependencies_json=dependencies_json))


def property_list_download(request, plist_id):
    """
    Fetches one plist and converts it to plist format (xml based)
    From: property_list/<plist_id>/download/
    :param request: 
    :param plist_id: 
    :return:
    """
    try:
        plist = PropertyList.objects.get(id=plist_id)
        plist = plist.generate()
    except PropertyList.DoesNotExist:
        return HttpResponse(status=404)
    return render(request, 'public_gate/property_list_download.html', dict(plist=plist), content_type="application/xml")


def add_property_list(request):
    """
    Adds one property list
    From: property_list/add/
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PropertyListForm(request.POST)
        print("POST property")
        if form.is_valid():
            form.save()
            form = PropertyListForm()
    else:
        form = PropertyListForm()
    return render(request, 'public_gate/property_list_add.html', dict(form=form))


########################################################################
#                                                                      #
#                           User Views
#                                                                      #
########################################################################


def users(request):
    """
    Fetches all users
    From: user/
    :param request:
    :return render:
    """
    users = User.objects.order_by('id')
    context = {'users': users}
    return render(request, 'public_gate/users.html', context)


def user_detail(request, user_id):
    """
    Fetches one user
    From: user/<user_id>/
    :param request:
    :param user_id:
    :return render:
    """
    try:
        user = User.objects.get(id=user_id)
    except PropertyList.DoesNotExist:
        return HttpResponse(status=404)
    return render(request, 'public_gate/user_detail.html', dict(user=user))


def add_user(request):
    """
    Adds one user
    From: user/add/
    :param request:
    :return render:
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'public_gate/user_add.html', dict(form=form))
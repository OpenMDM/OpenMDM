from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib.auth.hashers import (
    make_password)
from OpenMDM import settings
from common.local.settings import CONFIG
from common.utils import Recipe
import plistlib
import os



from public_gate.models import PropertyList, PropertyListForm, UserForm, Address, Test, RecipeForm


def home(request):
    """
    Displays home page
    :param request:
    :return render:
    """
    test = Test(username="Romain", date_inscription="2014-07-07", address=Address(city="Paris", street="Water street", zip="75016"))
    test.save()
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


def test(request):
    """
    Displays an example form, created from a hard-coded recipe (in recipe folder).
    This is for testing purpose only
    From : test/
    :param request:
    :return render:
    """
    if request.method == 'POST':
        # print(request.POST)
        form = RecipeForm(recipe_name="recipe.plist",
                          data=request.POST)
        #if form.is_valid():
        #    form.save()
        #    form = PropertyListForm()
        form = RecipeForm("recipe.plist").get_form()
    else:
        form = RecipeForm("recipe.plist").get_form()

    return render(request, 'public_gate/test.html', dict(form=form))


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
        user = None
        user_login = request.POST['login']
        user_password = request.POST['password']
        if user_login != "" and user_password != "":
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
    return render(request, 'public_gate/property_lists.html', dict(property_lists=property_lists))


def property_lists_for_user(request):
    """
    Fetches plists for specific user
    From: user/<user_id>/property_list/
    :param request:
    :param user_id:
    :return render:
    """
    property_lists = {}
    if settings.RETRIEVE_PLIST_FROM_GROUPS == "all":
        groups = request.user.ldap_user.group_names
    else:
        groups = {request.user.ldap_user.attrs['gidnumber'][0]}
    print(groups)
    #try:
    #    property_lists = PropertyList.objects.get(group_name=user_id)
    #except PropertyList.DoesNotExist:
    #    return HttpResponse(status=404)
    return render(request, 'public_gate/property_lists.html', dict(property_lists=property_lists))


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
    return render(request, 'public_gate/users.html', dict(users=users))


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
            # Creates hash with django make_password method
            form.instance.password = make_password(form.instance.password)
            form.save()
    else:
        form = UserForm()
    return render(request, 'public_gate/user_add.html', dict(form=form))
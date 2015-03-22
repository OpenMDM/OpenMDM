from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from OpenMDM import settings
import os
from public_gate.models import RecipeForm, Recipe


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
        print("login post")
        user = None
        user_login = request.POST['login']
        user_password = request.POST['password']
        print(user_login + " " + user_password)
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
    property_lists = Recipe.objects.all()
    return render(request, 'public_gate/property_lists.html', dict(property_lists=dict(all=property_lists)))


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
    for group in groups:
        plists = Recipe.objects(group_name=group)
        if len(plists) > 0:
            for plist in plists:
                plist.id = str(plist.id)
            property_lists[group] = Recipe.objects(group_name=group)

    return render(request, 'public_gate/property_lists.html', dict(property_lists=property_lists))


def property_list_detail(request, plist_id):
    """
    Fetches one plist
    From: property_list/<plist_id>/
    :param request: 
    :param plist_id: 
    :return render:
    """

    plist = Recipe.objects(id=plist_id)
    return render(request, 'public_gate/property_list_detail.html', dict(plist=plist[0]))


def property_list_download(request, plist_id):
    """
    Fetches one plist and converts it to plist format (xml based)
    From: property_list/<plist_id>/download/
    :param request: 
    :param plist_id: 
    :return:
    """
    plist = Recipe.objects(id=plist_id)
    plist = plist[0].generate()
    response = render(request, 'public_gate/property_list_download.html', dict(plist=plist), content_type="application/x-apple-aspen-config")
    response['Content-Disposition'] = "attachment; filename='{plist_id}.mobileconfig'".format(plist_id=plist_id)
    return response


def add_property_list(request):
    """
    Adds one property list
    From: property_list/add/
    :param request:
    :return:
    """
    form = False
    files = False
    if request.method == 'POST' and "file" in request.POST:
        form = RecipeForm(request.POST.get('file')).html_output()
    else:
        if request.method == 'POST':
            # We save the plist
            file_name = request.POST.get('recipe_file')
            form = RecipeForm(recipe_name=file_name,
                              data=request.POST)
            form.save()
            form = False

        # We display all the recipes available
        files = []
        for file in os.listdir(os.path.dirname(__file__) + "/../recipe"):
            if file.endswith(".plist"):
                files.append(file)
    return render(request, 'public_gate/property_list_add.html', dict(files=files,
                                                                      form=form))
import inspect
import os
import plistlib
import sys
import uuid
from plistlib import dumps
import re

from django.contrib.auth.models import User

from django.db import models
from django import forms
from mongoengine import *
from common.local.settings import CONFIG

from common.utils.PropertyList import format_object_to_plist


class Address(EmbeddedDocument):
    street = StringField(max_length=100)
    city = StringField(max_length=100)
    zip = IntField()


class Test(Document):
    username = StringField(max_length=100)
    date_inscription = DateTimeField(help_text='Sign-in date')
    address = EmbeddedDocumentField(Address)






class BaseModel(models.Model):
    """
    Describes base attributes for any property
    """
    payload_display_name = models.CharField(max_length=100)
    payload_description = models.CharField(max_length=100)
    payload_identifier = models.CharField(max_length=100, unique=True)
    payload_organization = models.CharField(max_length=100)
    payload_version = models.CharField(max_length=100)
    payload_uuid = models.CharField(max_length=100, default=str(uuid.uuid1()).upper())

    class Meta:
        abstract = True


class PropertyList(BaseModel):
    """
    Describes primary property
    """
    payload_type = models.CharField(max_length=13, editable=False, default="Configuration")
    removal_disallowed = models.CharField(max_length=15, choices=(('never', "Never"),
                                                                  ('authorization', "With authorization"),
                                                                  ('always', "Always")))

    def __str__(self):
        return self.payload_display_name + " - " + self.payload_description

    def save(self, *args, **kwargs):
        super(PropertyList, self).save(*args, **kwargs)

    def get_dependent_properties(self):
        dependencies = []
        for name, obj in (inspect.getmembers(sys.modules[__name__])):
            if re.match("[A-Za-z]*Property$", name):
                # Checking for all modules ending with "Property"
                try:
                    prop = obj.objects.get(property_list_id=self.id)
                    dependencies.append(prop)
                except obj.DoesNotExist:
                    print("This property does not have " + name)
        return dependencies


    def generate(self):
        """
        Generate an plist file from a PropertyList object
        """
        result = format_object_to_plist(self)
        result['payloadContent'] = []
        for name, obj in (inspect.getmembers(sys.modules[__name__])):
            # iOS properties name are only composed by letters, explaining [A-Za-z]
            if re.match("[A-Za-z]*Property$", name):
                # Checking for all modules ending with "Property"
                try:
                    prop = obj.objects.get(property_list_id=self.id)
                    prop = format_object_to_plist(prop)
                    result['payloadContent'].append(prop)
                except obj.DoesNotExist:
                    print("This property does not have " + name)
        return dumps(result)


class EmailAccountProperty(BaseModel):
    """
    Describes all necessary properties for mail configuration
    """
    property_list = models.OneToOneField(PropertyList)
    payload_type = models.CharField(max_length=22, editable=False, default="com.apple.mail.managed")
    email_account_description = models.CharField(max_length=100)
    email_account_name = models.CharField(max_length=100)
    email_account_type = models.CharField(max_length=15, choices=(
        ("EmailTypePOP", "POP"),
        ("EmailTypeIMAP", "IMAP")))
    email_address = models.CharField(max_length=100)
    incoming_mail_server_authentication = models.CharField(max_length=20, choices=(
        ("EmailAuthNone", "None"),
        ("EmailAuthPassword", "Password"),
        ("EmailAuthCRAMMD5", "MD5 challenge"),
        ("EmailAuthNTLM", "NTLM"),
        ("EmailAuthHTTPMD5", "Condensed MD5 HTTP")))
    incoming_mail_server_host_name = models.CharField(max_length=100)
    incoming_mail_server_IMAP_prefix = models.CharField(max_length=100)
    incoming_mail_server_port_number = models.IntegerField(default=143)
    incoming_mail_server_use_SSL = models.BooleanField(default=False)
    incoming_mail_server_user_name = models.CharField(max_length=100)
    incoming_password = models.CharField(max_length=100)
    outgoing_mail_server_authentication = models.CharField(max_length=20, choices=(
        ("EmailAuthNone", "None"),
        ("EmailAuthPassword", "Password"),
        ("EmailAuthCRAMMD5", "MD5 challenge"),
        ("EmailAuthNTLM", "NTLM"),
        ("EmailAuthHTTPMD5", "Condensed MD5 HTTP")))
    outgoing_mail_server_host_name = models.CharField(max_length=100)
    outgoing_mail_server_port_number = models.IntegerField(default=587)
    outgoing_mail_server_user_SSL = models.BooleanField(default=False)
    outgoing_mail_server_user_name = models.CharField(max_length=100)
    outgoing_password = models.CharField(max_length=100)
    outgoing_password_same_as_incoming_password = models.BooleanField(default=True)
    prevent_app_sheet = models.BooleanField(default=False)
    prevent_move = models.BooleanField(default=False)
    SMIME_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.email_account_name + " - " + self.email_account_description

    def save(self, *args, **kwargs):
        super(EmailAccountProperty, self).save(*args, **kwargs)
        
        
class RestrictionsProperty(BaseModel):
    """
    Describes all restrictions properties
    """
    property_list = models.OneToOneField(PropertyList)
    payload_type = models.CharField(max_length=28, editable=False, default="com.apple.applicationaccess")
    allow_adding_game_center_friends = models.BooleanField(default=True)
    allow_app_installation = models.BooleanField(default=True)
    allow_assistant = models.BooleanField(default=True)
    allow_assistant_while_locked = models.BooleanField(default=True)
    allow_bookstore_erotica = models.BooleanField(default=True)
    allow_camera = models.BooleanField(default=True)
    allow_cloud_backup = models.BooleanField(default=True)
    allow_cloud_document_sync = models.BooleanField(default=True)
    allow_diagnostic_submission = models.BooleanField(default=True)
    allow_explicit_content = models.BooleanField(default=True)
    allow_global_background_fetch_when_roaming = models.BooleanField(default=True)
    allow_in_app_purchases = models.BooleanField(default=True)
    allow_multiplayer_gaming = models.BooleanField(default=True)
    allow_passbook_while_locked = models.BooleanField(default=True)
    allow_photo_stream = models.BooleanField(default=True)
    allow_safari = models.BooleanField(default=True)
    allow_screen_shot = models.BooleanField(default=True)
    allow_shared_stream = models.BooleanField(default=True)
    allow_untrusted_tLSPrompt = models.BooleanField(default=True)
    allow_video_conferencing = models.BooleanField(default=True)
    allow_voice_dialing = models.BooleanField(default=True)
    allow_you_tube = models.BooleanField(default=True)
    allow_iTtunes = models.BooleanField(default=True)
    force_encrypted_backup = models.BooleanField(default=True)
    force_iTunes_store_password_entry = models.BooleanField(default=True)
    rating_apps = models.BooleanField(default=True)
    rating_movies = models.BooleanField(default=True)
    rating_region = models.BooleanField(default=True)
    rating_tVShows = models.BooleanField(default=True)
    safari_accept_cookies = models.BooleanField(default=True)
    safari_allow_auto_fill = models.BooleanField(default=True)
    safari_allow_java_script = models.BooleanField(default=True)
    safari_allow_popups = models.BooleanField(default=True)
    safari_force_fraud_warning = models.BooleanField(default=True)

    def __str__(self):
        return self.email_account_name + " - " + self.email_account_description

    def save(self, *args, **kwargs):
        super(RestrictionsProperty, self).save(*args, **kwargs)


class PropertyListForm(forms.ModelForm):
    class Meta:
        model = PropertyList
        fields = ['payload_display_name',
                  'payload_description',
                  'payload_identifier',
                  'payload_organization',
                  'payload_version',
                  'removal_disallowed'
                  ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',
                  'is_superuser',
                  'is_staff'
                  ]


class Plist(DynamicDocument):
    file_location = StringField(max_length=200)
    group_name = StringField(max_length=100)

    def __str__(self):
        return "Plist " + str(self.file_location) + " for group " + str(self.group_name)

    def generate(self):
        """
        Generate an plist file from a PropertyList object
        """
        dictionary = self.to_mongo().to_dict()
        dictionary['_id'] = str(dictionary['_id'])
        result = {'payloadContent': dictionary}
        return dumps(result)


class RecipeForm():
    def __init__(self, recipe_name=None, data=None):
        self.recipe_path = os.path.dirname(__file__) + "/../recipe/" + recipe_name
        self.recipe_dict = plistlib.load(open(self.recipe_path, 'rb'), fmt=plistlib.FMT_XML)
        self.form_answer = {}
        self.plist = Plist()
        # If form is filled out
        if data is not None:

            # We parse the expected outputs from the recipe
            for key, value in self.recipe_dict['outputs'].items():

                # And we fill an answer dictionary (in case of roll back)
                self.form_answer[key] = self.get_value_from_post_data(value, data)
                setattr(self.plist, key, self.get_value_from_post_data(value, data))

            # Then we add hook information
            self.plist.file_location = self.recipe_path
            self.plist.group_name = data.get("group_id")

    def get_value_from_post_data(self, value, data):
        # $key?(yes):(no)
        match = re.search("^\$(.*)\?\((.*)\):\((.*)\)$", value)
        if match:
            values = dict(key=match.group(1),
                          yes=match.group(2),
                          no=match.groups(3))
            if values['key'] in data:
                return self.get_value_from_post_data(values['yes'], data)
            else:
                return self.get_value_from_post_data(values['no'], data)

        # $key?(yes):
        match = re.search("^\$(.*)\?\((.*)\):$", value)
        if match:
            values = dict(key=match.group(1),
                          yes=match.group(2))
            if values['key'] in data:
                return self.get_value_from_post_data(values['yes'], data)
            return None

        # $key?:(no)
        match = re.search("^\$(.*)\?:\((.*)\)$", value)
        if match:
            values = dict(key=match.group(1),
                          no=match.group(2))
            if values['key'] not in data:
                return self.get_value_from_post_data(values['no'], data)
            return None

        # $key?
        match = re.search("^\$(.*)\?$", value)
        if match:
            values = dict(key=match.group(1))
            if values['key'] in data:
                return self.get_value_from_post_data("$" + values['key'], data)
            return None

        # $key
        match = re.search("^\$(.*)", value)
        if match:
            values = dict(key=match.group(1))
            if values['key'] in data:
                return data[values['key']]
            return None

        # @constant
        match = re.search("^@(.*)", value)
        if match:
            return match.group(1)

        # <hex>
        match = re.search("^<(.*)>$", value)
        if match:
            return match.group(1)

    def save(self):
        self.plist.save()

    @staticmethod
    def display_input(input_type, key, required, values, default_value, saved_value):
        """
        Creates HTML input, depending of the entry type
        :param input_type:
        :param key:
        :param required:
        :param values:
        :param default_value:
        :return string:
        """
        current_input = '<input type="{type}" ' \
                        'class="{input_class}" ' \
                        'name="{name}"' \
                        '{required}' \
                        '{checked} ' \
                        'value="{value}" ' \
                        'id="{id}">'
        if input_type == "string":
            current_input = current_input.format(id=key,
                                                 type="text",
                                                 input_class="form-control",
                                                 name=key,
                                                 required=" required" if required else "",
                                                 checked="",
                                                 value=saved_value if saved_value is not None
                                                 else default_value if default_value is not None
                                                 else "")
        if input_type == "boolean":
            current_input = current_input.format(id=key,
                                                 type="checkbox",
                                                 input_class="",
                                                 name=key,
                                                 required="",
                                                 checked=" checked" if saved_value is not None and saved_value
                                                 else "" if saved_value is not None and not saved_value
                                                 else " checked" if default_value
                                                 else "",
                                                 value="True")
        if input_type == "integer":
            current_input = current_input.format(id=key,
                                                 type="number",
                                                 input_class="form-control",
                                                 name=key,
                                                 required=" required" if required else "",
                                                 checked="",
                                                 value=saved_value if saved_value is not None
                                                 else default_value if default_value is not None
                                                 else "")
        if input_type == "list":
            select = []
            select.append('<select class="form-control" name="{name}"{required} id="{id}">'.format(name=key,
                                                                                             required=" required"
                                                                                             if required
                                                                                             else "",
                                                                                             id=key))
            for value in values:
                select.append('<option value="{value}"{selected}>'.format(value=value['value'],
                                                                     selected=" selected"
                                                                     if saved_value == value['value']
                                                                     else ""))

                select.append(value['title'])
                select.append("</option>")
            select.append('</select>')
            current_input = "\n".join(select)
        return current_input

    @staticmethod
    def check_key(obj, key):
        """
        Checks if key exists in dictionary, returns None if it doesn't
        :param obj:
        :param key:
        :return object:
        """
        return None if key not in obj.keys() else obj[key]

    @staticmethod
    def create_form(obj, form):
        """
        Create the html form from a python dictionary
        :param obj:
        :param form:
        :return string:
        """
        if type(obj).__name__ == "dict":
            if "type" in obj.keys():
                if obj['type'] == "group":
                    form.append('<fieldset><legend>{title}</legend>'.format(title=obj['title']))
                    form = RecipeForm.create_form(obj['content'], form)
                    form.append('</fieldset>')
                else:
                    form.append('<div class="form-group">')
                    label = '<label'
                    if obj['type'] != "boolean":
                        label += ' for="{id}"'.format(id=obj['key'])
                        label += '>{title}</label>'.format(title=obj['title'])
                    else:
                        label += '>'
                    form.append(label)

                    if RecipeForm.check_key(obj, "description") is not None:
                        form.append('<p class="help-block">{description}</p>'.format(description=obj['description']))
                    form.append(RecipeForm.display_input(input_type=obj['type'],
                                                     key=RecipeForm.check_key(obj, "key"),
                                                     required=RecipeForm.check_key(obj, "required"),
                                                     values=RecipeForm.check_key(obj, "values"),
                                                     default_value=RecipeForm.check_key(obj, "default_value"),
                                                     saved_value=None))
                    if obj['type'] == "boolean":
                        form.append(' {title}</label>'.format(title=obj['title']))
                    form.append('</div>')
            else:
                for key, value in obj.items():
                    if type(value).__name__ in ("dict", "list"):
                        form = RecipeForm.create_form(value, form)
        else:
            for value in obj:
                if type(value).__name__ in ("dict", "list"):
                    form = RecipeForm.create_form(value, form)
        return form

    def html_output(self):
        form = RecipeForm.create_form(self.recipe_dict, [])
        form.append('<div class="form-group">')
        form.append('<label for=group_id>Applies to group</label>')
        form.append('<select class="form-control" name="group_id" required id="group_id">')
        for group in CONFIG['local']['ldap']['GROUPS']:
            form.append('<option value="{value}">'.format(value=group))
            form.append(group)
            form.append("</option>")
        form.append('</select>')
        form.append('</div>')
        return "\n".join(form)
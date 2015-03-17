import inspect
import sys
from plistlib import dumps
from django.contrib.auth.models import User

from django.db import models
import re
from common.utils.PropertyList import format_object_to_plist
from django import forms


class BaseModel(models.Model):
    """
    Describes base attributes for any property
    """
    payload_display_name = models.CharField(max_length=100)
    payload_description = models.CharField(max_length=100)
    payload_identifier = models.CharField(max_length=100, unique=True)
    payload_organization = models.CharField(max_length=100)
    payload_version = models.CharField(max_length=100)
    payload_uuid = models.CharField(max_length=100, unique=True)

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
        exclude = []


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
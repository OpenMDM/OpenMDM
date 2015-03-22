import os
import plistlib
from plistlib import dumps
import uuid
import re

from django.contrib.auth.models import User
from mongoengine import *
from common.local.settings import CONFIG
from common.utils.Utils import str_to_bool


class CustomPlist(DynamicEmbeddedDocument):
    PayloadUUID = StringField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.PayloadUUID = str(uuid.uuid1()).upper()


class Plist(EmbeddedDocument):
    PayloadDisplayName = StringField(max_length=100)
    PayloadDescription = StringField(max_length=100)
    PayloadIdentifier = StringField(max_length=100)
    PayloadOrganization = StringField(max_length=100)
    PayloadRemovalDisallowed = BooleanField(default=True)
    PayloadType = StringField(max_length=100)
    PayloadUUID = StringField(max_length=100)
    PayloadVersion = StringField(max_length=100)
    PayloadContent = ListField(EmbeddedDocumentField(CustomPlist))

    def __init__(self, recipe=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if recipe is not None:
            self.PayloadDisplayName = recipe.get('PayloadDisplayName', '<no name>')
            self.PayloadDescription = recipe.get('PayloadDescription', '<no description>')
            self.PayloadIdentifier = recipe.get('PayloadIdentifier', '<no identifier>')
            self.PayloadOrganization = recipe.get('PayloadOrganization', '<no organization>')
            self.PayloadRemovalDisallowed = recipe.get(str_to_bool('PayloadRemovalDisallowed'), False)
            self.PayloadType = recipe.get('PayloadType', '<no type>')
            self.PayloadUUID = str(uuid.uuid1()).upper()
            self.PayloadVersion = str(recipe.get('PayloadVersion', '<no version>'))


class Recipe(Document):
    group_name = StringField(max_length=100)
    plist = EmbeddedDocumentField(Plist)

    def generate(self):
        """
        Generate an plist file from a PropertyList object
        """
        recipe = self.to_mongo().to_dict()
        plist = recipe['plist']

        return dumps(plist)


class RecipeForm():
    base_recipe_dict = None
    recipe_dict = None
    recipe_name = None

    def __init__(self, recipe_name=None, data=None):
        self.recipe_name = recipe_name
        self.plist = Plist()
        self.recipe = Recipe()
        self.base_recipe_dict = RecipeForm.get_dict_from_recipe_name("base.xml")
        self.recipe_dict = RecipeForm.get_dict_from_recipe_name(self.recipe_name)
        self.plist = Plist(self.recipe_dict)
        # If form is filled out
        if data is not None:
            custom_plist = CustomPlist()
            # We parse the expected outputs from the recipe
            for key, value in self.base_recipe_dict['outputs'].items():
                setattr(custom_plist, key, self.get_value_from_post_data(value, data, type(value)))
            for key, value in self.recipe_dict['outputs'].items():
                setattr(custom_plist, key, self.get_value_from_post_data(value, data, type(value)))

            # Then we add recipe information
            self.plist.PayloadContent.append(custom_plist)
            self.plist.PayloadRemovalDisallowed = str_to_bool(data.get("PayloadRemovalDisallowed", False))
            self.recipe.group_name = data.get("group_id")
            self.recipe.plist = self.plist

    def save(self):
        self.recipe.save()

    @staticmethod
    def get_dict_from_recipe_name(recipe_name):
        recipes_directory = os.path.normpath(os.path.dirname(__file__) + "/../recipe/") + "/"

        # We get the required recipe
        recipe_path = recipes_directory + recipe_name

        # We get is as dict
        recipe_dict = plistlib.load(open(recipe_path, 'rb'), fmt=plistlib.FMT_XML)

        return recipe_dict

    def get_value_from_post_data(self, value, data, data_type):
        # $key?(yes):(no)
        match = re.search("^\$(.*)\?\((.*)\):\((.*)\)$", value)
        if match:
            values = dict(key=match.group(1),
                          yes=match.group(2),
                          no=match.groups(3))
            if values['key'] in data:
                return self.get_value_from_post_data(values['yes'], data, data_type)
            else:
                return self.get_value_from_post_data(values['no'], data, data_type)

        # $key?(yes):
        match = re.search("^\$(.*)\?\((.*)\):$", value)
        if match:
            values = dict(key=match.group(1),
                          yes=match.group(2))
            if values['key'] in data:
                return self.get_value_from_post_data(values['yes'], data, data_type)
            return None

        # $key?:(no)
        match = re.search("^\$(.*)\?:\((.*)\)$", value)
        if match:
            values = dict(key=match.group(1),
                          no=match.group(2))
            if values['key'] not in data:
                return self.get_value_from_post_data(values['no'], data, data_type)
            return None

        # $key?
        match = re.search("^\$(.*)\?$", value)
        if match:
            values = dict(key=match.group(1))
            if values['key'] in data:
                return self.get_value_from_post_data("$" + values['key'], data, data_type)
            return None

        # $key
        match = re.search("^\$(.*)", value)
        if match:
            values = dict(key=match.group(1))
            if values['key'] in data:
                return data[values['key']]
            return None

        # @UUID
        match = re.search("^@UUID$", value)
        if match:
            return str(uuid.uuid1()).upper()

        # @constant
        match = re.search("^@(.*)", value)
        if match:
            return match.group(1)

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
        elif input_type == "boolean":
            # Hack for posting checkbox even if it's unchecked. Hidden input value will be used in case of
            # the checkbox is unchecked
            hidden_input = '<input type="hidden" ' \
                           'name="{name}"' \
                           'value="{value}">'.format(name=key,
                                                     value="False")
            current_input = hidden_input + current_input.format(id=key,
                                                                type="checkbox",
                                                                input_class="",
                                                                name=key,
                                                                required="",
                                                                checked=" checked" if saved_value is not None and saved_value
                                                                else "" if saved_value is not None and not saved_value
                                                                else " checked" if default_value
                                                                else "",
                                                                value="True")
        elif input_type == "integer":
            current_input = current_input.format(id=key,
                                                 type="number",
                                                 input_class="form-control",
                                                 name=key,
                                                 required=" required" if required else "",
                                                 checked="",
                                                 value=saved_value if saved_value is not None
                                                 else default_value if default_value is not None
                                                 else "")
        elif input_type == "list":
            select = ['<select class="form-control" name="{name}"{required} id="{id}">'.format(name=key,
                                                                                               required=" required"
                                                                                               if required
                                                                                               else "",
                                                                                               id=key)]
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
    def create_form(obj, form):
        """
        Create the html form from a python dictionary
        :param obj:
        :param form:
        :return string:
        """
        if type(obj).__name__ == "dict":
            if "type" in obj.keys() and "title" in obj.keys():
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

                    if obj.get('description', False):
                        form.append('<p class="help-block">{description}</p>'.format(description=obj['description']))
                    form.append(RecipeForm.display_input(input_type=obj['type'],
                                                         key=obj.get('key', None),
                                                         required=obj.get('required', None),
                                                         values=obj.get('values', None),
                                                         default_value=obj.get('default_value', None),
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
        form = ['<fieldset><legend>{title}</legend>'.format(title="General description")]
        form = RecipeForm.create_form(self.base_recipe_dict, form)
        form.append('</fieldset>')
        form.append('<fieldset><legend>{title}</legend>'.format(title="Content"))
        form = RecipeForm.create_form(self.recipe_dict, form)
        form.append('<div class="form-group">')
        form.append('<label for=group_id>Applies to group</label>')
        form.append('<select class="form-control" name="group_id" required id="group_id">')
        for group in CONFIG['local']['ldap']['GROUPS']:
            form.append('<option value="{value}">'.format(value=group))
            form.append(group)
            form.append("</option>")
        form.append('</select>')
        form.append('</div>')
        form.append('</fieldset>')
        form.append('<input type="hidden" name="recipe_file" value="{value}" />'.format(value=self.recipe_name))
        return "\n".join(form)

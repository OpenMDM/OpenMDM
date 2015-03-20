from common.local.settings import CONFIG


def display_input(input_type, key, required, values, default_value):
    """
    Creates HTML input, depending of the entry type
    :param input_type:
    :param key:
    :param required:
    :param values:
    :param default_value:
    :return string:
    """
    input = '<input type="{type}" class="{input_class}" name="{name}"{required}{checked} value="{value}" id="{id}">'
    if input_type == "string":
        input = input.format(id=key,
                             type="text",
                             input_class="form-control",
                             name=key,
                             required=" required" if required else "",
                             checked="",
                             value=default_value if default_value is not None else "")
    if input_type == "boolean":
        input = input.format(id=key,
                             type="checkbox",
                             input_class="",
                             name=key,
                             required="",
                             checked=" checked" if default_value  else "",
                             value="True")
    if input_type == "integer":
        input = input.format(id=key,
                             type="number",
                             input_class="form-control",
                             name=key,
                             required=" required" if required else "",
                             checked="",
                             value=default_value if default_value is not None else "")
    if input_type == "list":
        input = '<select class="form-control" name="{name}"{required} id="{id}">'.format(name=key,
                                                                                         required=" required"
                                                                                         if required
                                                                                         else "",
                                                                                         id=key)
        for value in values:
            input += '<option value="{value}">'.format(value=value['value'])
            input += value['title']
            input += "</option>"
        input += '</select>'
    return input


def check_key(obj, key):
    """
    Checks if key exists in dictionary, returns None if it doesn't
    :param obj:
    :param key:
    :return object:
    """
    return None if key not in obj.keys() else obj[key]


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
                form += '<fieldset><legend>{title}</legend>'.format(title=obj['title'])
                form = create_form(obj['content'], form)
                form += '</fieldset>'
            else:
                form += '<div class="form-group">'
                form += '<label'
                if obj['type'] != "boolean":
                    form += ' for="{id}"'.format(id=obj['key'])
                    form += '>{title}</label>'.format(title=obj['title'])
                else:
                    form += '>'

                if check_key(obj, "description" is not None):
                    form += '<p class="help-block">{description}</p>'.format(description=obj['description'])
                form += display_input(input_type=obj['type'],
                                      key=check_key(obj, "key"),
                                      required=check_key(obj, "required"),
                                      values=check_key(obj, "values"),
                                      default_value=check_key(obj, "default_value"))
                if obj['type'] == "boolean":
                    form += ' {title}</label>'.format(title=obj['title'])
                form += '</div>'
        else:
            for key, value in obj.items():
                if type(value).__name__ in ("dict", "list"):
                    form = create_form(value, form)
    else:
        for value in obj:
            if type(value).__name__ in ("dict", "list"):
                form = create_form(value, form)
    return form


def get_form_from_dictionary(dictionary):
    form = create_form(dictionary, "")
    form += '<div class="form-group">'
    form += '<label for=group_id>Applies to group</label>'
    form += '<select class="form-control" name="group_id" required id="group_id">'
    for group in CONFIG['local']['ldap']['GROUPS']:
        form += '<option value="{value}">'.format(value=group)
        form += group
        form += "</option>"
    form += '</select>'
    form += '</div>'
    return form
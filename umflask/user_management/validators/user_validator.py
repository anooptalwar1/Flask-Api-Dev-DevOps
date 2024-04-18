import re
from user_management.constants import api_constants
from user_management.constants import app_constants
from user_management.constants import db_constants


def check_attributes(dictionary, keys):
    """Generic method to check whether all the keys are present in the dictionary or not"""

    for key in keys:
        if key not in dictionary:
            return "Attribute '{}' is missing in request".format(key)

    return ''


def validate_insert_user(user):
    attribute_msg = check_attributes(
        user, api_constants.USER_POST_ATTRIBUTES_LIST)
    if attribute_msg:
        return attribute_msg
    else:
        message = "Invalid value '{}' for attribute '{}' in request"

        key = api_constants.USER_POST_ATTRIBUTE_NAME
        value = user[key]
        if not value:
            return message.format(value, key)

        key = api_constants.USER_POST_ATTRIBUTE_EMAIL
        value = user[key]
        if not value or not re.search(app_constants.EMAIL_REGEX, value):
            return message.format(value, key)

        key = api_constants.USER_POST_ATTRIBUTE_PASSWORD
        value = user[key]
        if not value:
            return message.format(value, key)

        key = api_constants.USER_POST_ATTRIBUTE_LEVEL
        if key in user:
            value = user[key]
            if not value or value not in db_constants.USER_LEVEL_ENUM_LIST:
                return message.format(value, key)

    return ''


def validate_login(credentials):
    attribute_msg = check_attributes(
        credentials, api_constants.USER_LOGIN_ATTRIBUTES_LIST)
    if attribute_msg:
        return attribute_msg
    else:
        for key in api_constants.USER_LOGIN_ATTRIBUTES_LIST:
            value = credentials[key].strip()
            if not value:
                return "Invalid value '{}' for attribute '{}' in request".format(value, key)

    return ''


def validate_update_user(user):
    if not isinstance(user, dict) or len(user) == 0:
        return "Provide some data to update"

    key = api_constants.ATTRIBUTE_ID
    if key in user:
        value = user[key]
        if not value or not value.isdigit():
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)

    has_valid_keys = False
    key = api_constants.USER_POST_ATTRIBUTE_NAME
    if key in user:
        has_valid_keys = True
        value = user[key]
        if not value:
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)

    old_password_key = api_constants.USER_POST_ATTRIBUTE_OLD_PASSWORD
    password_key = api_constants.USER_POST_ATTRIBUTE_PASSWORD
    if old_password_key in user and password_key in user:
        has_valid_keys = True
        old_password_value = user[old_password_key]
        password_value = user[password_key]
        if not old_password_value:
            return "Invalid value '{}' for attribute '{}' in request".format(old_password_value, old_password_key)
        if not password_value:
            return "Invalid value '{}' for attribute '{}' in request".format(password_value, password_key)
        if old_password_value == password_value:
            return "New and old password can't be same"

    if has_valid_keys:
        return ''
    else:
        return "Invalid parameters to update"


def validate_deactivate_user(user_id, user):
    if not isinstance(user, dict) or len(user) == 0:
        return "Attribute(s) missing in request"

    key = api_constants.ATTRIBUTE_ID
    if key in user:
        value = user[key]
        if not value or not value.isdigit():
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)
        elif int(user_id) == int(value):
            return "You cannot deactivate yourself"
    else:
        return "Attribute '{}' is missing in request".format(key)

    return ''

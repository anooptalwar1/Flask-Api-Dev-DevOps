import json
import re
from constants import api_constants
from constants import db_constants


def validate_procedure(procedure):
    for key in api_constants.PROCEDURE_POST_ATTRIBUTE_LIST:
        if key not in procedure:
            return "Attribute '{}' is missing in request".format(key)

        value = procedure[key]
        if isinstance(value, str):
            value = value.strip()
            procedure[key] = value

        if not value:
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)

        if key == api_constants.PROCEDURE_POST_ATTRIBUTE_STEPS:
            if not isinstance(value, list):
                return "Invalid value '{}' for attribute '{}' in request".format(value, key)

            is_invalid = validate_step(
                procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_STEPS])
            if is_invalid:
                return is_invalid

    return ''


def validate_step(steps):
    for index in range(len(steps)):
        step = steps[index]

        if api_constants.ATTRIBUTE_ID in step:
            value = step[api_constants.ATTRIBUTE_ID]
            if not value or not isinstance(value, int):
                return "Invalid value '{}' for attribute '{}' in request".format(value, api_constants.ATTRIBUTE_ID)

        for key in api_constants.STEP_POST_ATTRIBUTE_LIST:
            if key not in step:
                return "Attribute '{}' is missing in request".format(key)

            value = step[key]
            if isinstance(value, str):
                value = value.strip()
                step[key] = value

            if not value:
                return "Invalid value '{}' for attribute '{}' in request".format(value, key)

            if key == api_constants.STEP_POST_ATTRIBUTE_SEQUENCE_NUMBER:
                if not isinstance(value, int):
                    return "Invalid value '{}' for attribute '{}' in request".format(value, key)

            if key == api_constants.STEP_POST_ATTRIBUTE_TYPE:
                if value not in db_constants.STEP_TYPE_ENUM_LIST:
                    return "Invalid value '{}' for attribute '{}' in request".format(value, key)

                elif value == db_constants.STEP_TYPE_ENUM_VIDEO or value == db_constants.STEP_TYPE_ENUM_IMAGE:
                    if api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL not in step:
                        return "Attribute '{}' is missing in request".format(api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL)

                    type_value = step[api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL]
                    if isinstance(type_value, str):
                        type_value = type_value.strip()
                        step[api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL] = type_value

                    regex = re.compile(
                        r'^(?:http|ftp)s?://'  # http:// or https://
                        # domain...
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                        r'localhost|'  # localhost...
                        # ...or ip
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                        r'(?::\d+)?'  # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if not type_value or not re.match(regex, type_value):
                        return "Invalid value '{}' for attribute '{}' in request".format(type_value, api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL)

    return ''


def validate_add_procedure(procedure):
    is_invalid = validate_procedure(procedure)
    if is_invalid:
        return is_invalid
    else:
        return ''


def validate_update_procedure(procedure):
    is_invalid = validate_procedure(procedure)
    if is_invalid:
        return is_invalid
    else:
        return ''


def validate_get_all_procedure_names(headers):
    if api_constants.ATTRIBUTE_OBJECT_ID in headers:
        value = headers[api_constants.ATTRIBUTE_OBJECT_ID]
        if not value or not value.isdigit():
            return "Invalid value '{}' for attribute '{}' in request".format(value, api_constants.ATTRIBUTE_OBJECT_ID)
    elif api_constants.ATTRIBUTE_OBJECT_NAME in headers:
        value = headers[api_constants.ATTRIBUTE_OBJECT_NAME]
        if not value:
            return "Invalid value '{}' for attribute '{}' in request".format(value, api_constants.ATTRIBUTE_OBJECT_NAME)
    else:
        return "Please provide required valid header(s)"

    return ''

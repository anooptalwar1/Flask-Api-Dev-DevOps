from user_management.constants import db_constants
from user_management.constants import api_constants


def validate_update_session(user):
    if not isinstance(user, dict) or len(user) == 0:
        return "Provide some data to update"

    key = api_constants.ATTRIBUTE_ID
    if key in user:
        value = user[key]
        if not value:
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)
    else:
        return "Missing attribute '{}'".format(api_constants.ATTRIBUTE_ID)

    key = api_constants.SESSION_UPDATE_ATTRIBUTE_STATUS
    if key in user:
        value = user[key]
        if not value or value not in db_constants.UPDATE_SESSION_STATUS_ENUM_LIST:
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)
    else:
        return "Missing attribute '{}'".format(api_constants.SESSION_UPDATE_ATTRIBUTE_STATUS)

    key = api_constants.SESSION_UPDATE_ATTRIBUTE_DEVICE_TYPE
    if key in user:
        value = user[key]
        if not value or value not in db_constants.SESSION_DEVICE_TYPE_ENUM_LIST:
            return "Invalid value '{}' for attribute '{}' in request".format(value, key)
    else:
        return "Missing attribute '{}'".format(api_constants.SESSION_UPDATE_ATTRIBUTE_DEVICE_TYPE)

    if user[api_constants.SESSION_UPDATE_ATTRIBUTE_DEVICE_TYPE] == db_constants.SESSION_DEVICE_TYPE_ENUM_HOLOLENS:
        key = api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_USERNAME
        if key in user:
            value = user[key]
            if not value:
                return "Invalid value '{}' for attribute '{}' in request".format(value, key)
        else:
            return "Missing attribute '{}'".format(api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_USERNAME)

        key = api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_PASSWORD
        if key in user:
            value = user[key]
            if not value:
                return "Invalid value '{}' for attribute '{}' in request".format(value, key)
        else:
            return "Missing attribute '{}'".format(api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_PASSWORD)

    return ''

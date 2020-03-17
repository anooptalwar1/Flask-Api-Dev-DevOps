from user_management.models import session_model
from user_management.validators import session_validator
from user_management.utils import app_utils
from user_management.constants import api_constants


def update_session(ip_address, session):
    is_invalid = session_validator.validate_update_session(session)
    if is_invalid:
        return app_utils.get_message_json_obj(is_invalid), ''
    else:
        user_id = session[api_constants.ATTRIBUTE_ID]
        device_type = session_model.update_session(user_id, ip_address, session)
        if device_type == False:
            return app_utils.get_message_json_obj("Nothing to update"), ''
        elif device_type == None:
            return app_utils.get_message_json_obj("Invalid id '{}'".format(user_id)), ''
        else:
            return app_utils.get_message_json_obj("Session updated successfully"), device_type


def set_status_offline(ip_address):
    return session_model.set_status_offline(ip_address)


def get_online_hololens_users():
    return session_model.get_online_hololens_users()


def get_online_android_users():
    return session_model.get_online_android_users()
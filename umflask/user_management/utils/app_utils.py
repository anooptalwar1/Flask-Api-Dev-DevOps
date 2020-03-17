from flask_api import status
from user_management.constants import db_constants


def get_message_json_obj(message):
    error = {}
    error['message'] = message
    return error


def get_response_code(app_internal_code):
    return {
        db_constants.ERROR_CODE_DUPLICATE_ENTRY: status.HTTP_409_CONFLICT
    }.get(app_internal_code, status.HTTP_400_BAD_REQUEST)

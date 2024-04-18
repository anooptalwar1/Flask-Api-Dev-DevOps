from flask import jsonify
from flask_api import status
from user_management.utils import app_utils
from user_management.controllers import user_controller
from user_management.controllers import session_controller
from user_management.constants import api_constants


def get_id_from_header(headers):
    if api_constants.ATTRIBUTE_ID in headers:
        user_id = headers[api_constants.ATTRIBUTE_ID]
        if user_id.isdigit():
            return int(user_id)
        else:
            return 0
    else:
        return 0


def insert_user(request):
    return user_controller.insert_user(request.form)


def login(request):
    return user_controller.login(request.form)


def get_all_users_for_user_id(request):
    user_id = get_id_from_header(request.headers)
    if not user_id:
        return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
    else:
        return user_controller.get_all_users_for_user_id(user_id)


def update_user(request):
    user_id = get_id_from_header(request.headers)
    if not user_id:
        return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
    else:
        return user_controller.update_user(request.form, user_id)


def deactivate_user(request):
    user_id = get_id_from_header(request.headers)
    if not user_id:
        return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
    else:
        return user_controller.deactivate_user(user_id, request.form)

import traceback
from flask import jsonify
from flask_api import status
from user_management.models import user_model
from user_management.validators import user_validator
from user_management.utils import app_utils


def insert_user(user):
    try:
        is_invalid = user_validator.validate_insert_user(user)
        if is_invalid:
            return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
        else:
            result = user_model.insert_user(user)
            if isinstance(result, Exception):
                return jsonify(app_utils.get_message_json_obj(result.orig.args[1])), app_utils.get_response_code(result.orig.args[0])
            else:
                return jsonify(result), status.HTTP_201_CREATED
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def login(credentials):
    try:
        is_invalid = user_validator.validate_login(credentials)
        if is_invalid:
            return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
        else:
            result = user_model.check_login_credentials(credentials)
            if not result:
                return jsonify(app_utils.get_message_json_obj("Invalid credentials")), status.HTTP_401_UNAUTHORIZED
            else:
                return jsonify(result), status.HTTP_200_OK
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def get_all_users_for_user_id(user_id):
    try:
        result = user_model.get_all_users_for_user_id(user_id)
        if result == None:
            return jsonify(app_utils.get_message_json_obj("Invalid id '{}'".format(user_id))), status.HTTP_400_BAD_REQUEST
        elif result == 0:
            return '', status.HTTP_204_NO_CONTENT
        else:
            return jsonify(result), status.HTTP_200_OK
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def update_user(user, user_id):
    try:
        is_invalid = user_validator.validate_update_user(user)
        if is_invalid:
            return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
        else:
            result = user_model.update_user(user, user_id)
            if result == None:
                return jsonify(app_utils.get_message_json_obj("Invalid id '{}'".format(user_id))), status.HTTP_400_BAD_REQUEST
            elif result == False:
                return jsonify(app_utils.get_message_json_obj("Old password does not match")), status.HTTP_400_BAD_REQUEST
            elif isinstance(result, int):
                return jsonify(app_utils.get_message_json_obj("Invalid id '{}'".format(result))), status.HTTP_400_BAD_REQUEST
            else:
                return jsonify(result), status.HTTP_200_OK
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def deactivate_user(user_id, user):
    try:
        is_invalid = user_validator.validate_deactivate_user(user_id, user)
        if is_invalid:
            return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST

        result = user_model.deactivate_user(user_id, user)
        if result == True:
            return jsonify(app_utils.get_message_json_obj("User deleted successfully")), status.HTTP_200_OK
        elif result == False:
            return jsonify(app_utils.get_message_json_obj("Invalid requestor id '{}'".format(user_id))), status.HTTP_400_BAD_REQUEST
        else:
            return jsonify(app_utils.get_message_json_obj("User not found for id '{}' to deactivate".format(result))), status.HTTP_400_BAD_REQUEST
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR

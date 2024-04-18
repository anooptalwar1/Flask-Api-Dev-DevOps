import traceback
from models import procedure_model
from flask import jsonify
from flask_api import status
from validators import procedure_validator
from utils import app_utils
from constants import api_constants


def get_id_from_header(headers):
    if api_constants.ATTRIBUTE_ID in headers:
        user_id = headers[api_constants.ATTRIBUTE_ID]
        if user_id.isdigit():
            return int(user_id)
        else:
            return 0
    else:
        return 0

def get_object_id_from_header(headers):
    if api_constants.ATTRIBUTE_OBJECT_ID in headers:
        object_id = headers[api_constants.ATTRIBUTE_OBJECT_ID]
        if object_id.isdigit():
            return int(object_id)
        else:
            return 0
    else:
        return 0


def get_all_object_names():
    try:
        objects = procedure_model.get_all_object_names()
        if len(objects) > 0:
            return jsonify(objects)
        else:
            return '', status.HTTP_204_NO_CONTENT
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def get_all_procedure_names(request):
    try:
        is_invalid = procedure_validator.validate_get_all_procedure_names(
            request.headers)
        if is_invalid:
            return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
        else:
            procedures = procedure_model.get_all_procedure_names(
                request.headers)
            if procedures == None:
                return jsonify(app_utils.get_message_json_obj(
                    "Invalid object id or name to fetch procedures")), status.HTTP_400_BAD_REQUEST
            elif len(procedures) > 0:
                return jsonify(procedures)
            else:
                return '', status.HTTP_204_NO_CONTENT
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def get_procedure_by_id(procedure_id):
    try:
        procedure = procedure_model.get_procedure_by_id(procedure_id)
        if procedure:
            return jsonify(procedure)
        else:
            return jsonify(app_utils.get_message_json_obj("Invalid procedure ID")), status.HTTP_400_BAD_REQUEST
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def add_procedure(request):
    try:
        user_id = get_id_from_header(request.headers)
        object_id = get_object_id_from_header(request.headers)
        if not user_id or not object_id:
            return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
        else:
            is_invalid = procedure_validator.validate_add_procedure(
                request.json)
            if is_invalid:
                return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
            else:
                inserted = procedure_model.insert_procedure(user_id, object_id, request.json)
                if not inserted:
                    return jsonify(app_utils.get_message_json_obj("Invalid object id")), status.HTTP_400_BAD_REQUEST
                else:
                    return jsonify(app_utils.get_message_json_obj("Procedure saved successfully"))
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def deactivate_procedure(request, procedure_id):
    try:
        user_id = get_id_from_header(request.headers)
        if not user_id:
            return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
        else:
            deactivated = procedure_model.deactivate_procedure(
                user_id, procedure_id)
            if deactivated:
                return jsonify(app_utils.get_message_json_obj("Procedure deleted successfully"))
            else:
                return jsonify(app_utils.get_message_json_obj("Invalid procedure ID")), status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR


def update_procedure(request, procedure_id):
    try:
        user_id = get_id_from_header(request.headers)
        if not user_id:
            return jsonify(app_utils.get_message_json_obj('Please provide required valid header(s)')), status.HTTP_400_BAD_REQUEST
        else:
            is_invalid = procedure_validator.validate_update_procedure(
                request.json)
            if is_invalid:
                return jsonify(app_utils.get_message_json_obj(is_invalid)), status.HTTP_400_BAD_REQUEST
            else:
                updated = procedure_model.update_procedure(
                    user_id, procedure_id, request.json)
                if updated:
                    return jsonify(app_utils.get_message_json_obj("Procedure updated successfully"))
                else:
                    return jsonify(app_utils.get_message_json_obj("Invalid procedure ID")), status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        print(traceback.format_exc())
        return jsonify(app_utils.get_message_json_obj("Something went wrong on server. Please contact support.")), status.HTTP_500_INTERNAL_SERVER_ERROR

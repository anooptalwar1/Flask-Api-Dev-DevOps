import time
from app import db, ma
from constants import db_constants
from constants import api_constants
from utils import db_utils


class Step(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.Text)
    type = db.Column(db.Enum(db_constants.STEP_TYPE_ENUM_TEXT,
                             db_constants.STEP_TYPE_ENUM_VIDEO,
                             db_constants.STEP_TYPE_ENUM_IMAGE), nullable=False,
                     default=db_constants.STEP_TYPE_ENUM_TEXT)
    sequence_number = db.Column(db.Integer, nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey(
        'procedure.id'), nullable=False)


class Procedure(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    spec_reference = db.Column(db.Text, nullable=False)
    dept = db.Column(db.Text, nullable=False)
    document_id = db.Column(db.Text, nullable=False)
    tools = db.Column(db.Text, nullable=False)
    safety_req = db.Column(db.Text, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    escalation_plan = db.Column(db.Text, nullable=False)
    updated_by_user_id = db.Column(db.Integer, nullable=False)
    is_deactive = db.Column(db.Integer, nullable=False, default=0)
    object_id = db.Column(db.Integer, db.ForeignKey(
        'object.id'), nullable=False)
    steps = db.relationship('Step', lazy='select', order_by=Step.sequence_number,
                            backref=db.backref('procedure', lazy='joined'))


class Object(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)


class StepSchema(ma.ModelSchema):
    class Meta:
        model = Step
        fields = ('id', 'name', 'description', 'media_url',
                  'type', 'sequence_number')
        sqla_session = db.session


class ProcedureSchema(ma.ModelSchema):
    class Meta:
        model = Procedure
        fields = ('id', 'name', 'spec_reference', 'dept', 'document_id',
                  'tools', 'safety_req', 'purpose', 'escalation_plan', 'steps')
        sqla_session = db.session
    steps = ma.Nested(StepSchema, many=True)


class ObjectSchema(ma.ModelSchema):
    class Meta:
        model = Object
        fields = ('id', 'name')
        sqla_session = db.session


def get_all_object_names():
    objects = Object.query.all()
    objects_schema = ObjectSchema(many=True)
    return objects_schema.dump(objects)


def get_all_procedure_names(_object):
    db_object = None
    if api_constants.ATTRIBUTE_OBJECT_ID in _object:
        object_id = _object[api_constants.ATTRIBUTE_OBJECT_ID]
        db_object = Object.query.filter(Object.id == object_id).first()
    else:
        object_name = _object[api_constants.ATTRIBUTE_OBJECT_NAME]
        db_object = Object.query.filter(Object.name == object_name).first()

    if not db_object:
        return None

    procedures = Procedure.query.filter(db.and_(
        Procedure.is_deactive == 0), (Procedure.object_id == db_object.id)).all()
    procedure_schema = ProcedureSchema(only=['id', 'name'], many=True)
    return procedure_schema.dump(procedures)


def get_procedure_by_id(procedure_id):
    procedure = Procedure.query.filter(
        db.and_(Procedure.id == procedure_id), (Procedure.is_deactive == 0)).first()
    if not procedure:
        return None
    else:
        procedure_schema = ProcedureSchema()
        return procedure_schema.dump(procedure)


def insert_procedure(user_id, object_id, procedure):
    db_object = Object.query.filter(Object.id == object_id).first()
    if not db_object:
        return None

    procedure_to_insert = Procedure(
        name=procedure[api_constants.ATTRIBUTE_NAME],
        spec_reference=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_SPEC_REFERENCE],
        dept=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_DEPT],
        document_id=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_DOCUMENT_ID],
        tools=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_TOOLS],
        safety_req=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_SAFETY_REQ],
        purpose=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_PURPOSE],
        escalation_plan=procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_ESCALATION_PLAN],
        updated_by_user_id=user_id,
        object_id=object_id
    )

    for step in procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_STEPS]:
        step_to_insert = Step(
            name=step[api_constants.ATTRIBUTE_NAME],
            type=step[api_constants.STEP_POST_ATTRIBUTE_TYPE],
            sequence_number=step[api_constants.STEP_POST_ATTRIBUTE_SEQUENCE_NUMBER],
            description=step[api_constants.STEP_POST_ATTRIBUTE_DESCRIPTION]
        )

        type_value = step[api_constants.STEP_POST_ATTRIBUTE_TYPE]
        if type_value == db_constants.STEP_TYPE_ENUM_VIDEO or type_value == db_constants.STEP_TYPE_ENUM_IMAGE:
            step_to_insert.media_url = step[api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL]

        procedure_to_insert.steps.append(step_to_insert)

    db.session.add(procedure_to_insert)
    db.session.commit()
    return True


def deactivate_procedure(user_id, procedure_id):
    procedure_to_update = Procedure.query.filter(
        db.and_(Procedure.id == procedure_id), (Procedure.is_deactive == 0)).first()
    if not procedure_to_update:
        return False
    else:
        procedure_to_update.is_deactive = 1
        procedure_to_update.updated_by_user_id = user_id
        db.session.commit()
        return True


def update_procedure(user_id, procedure_id, procedure):
    procedure_to_update = Procedure.query.filter(
        db.and_(Procedure.id == procedure_id), (Procedure.is_deactive == 0)).first()

    if not procedure_to_update:
        return False

    procedure_to_update.name = procedure[api_constants.ATTRIBUTE_NAME]
    procedure_to_update.spec_reference = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_SPEC_REFERENCE]
    procedure_to_update.dept = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_DEPT]
    procedure_to_update.document_id = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_DOCUMENT_ID]
    procedure_to_update.tools = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_TOOLS]
    procedure_to_update.safety_req = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_SAFETY_REQ]
    procedure_to_update.purpose = procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_PURPOSE]
    procedure_to_update.escalation_plan = procedure[
        api_constants.PROCEDURE_POST_ATTRIBUTE_ESCALATION_PLAN]
    procedure_to_update.updated_by_user_id = user_id

    steps_to_delete = []
    for db_step in procedure_to_update.steps:
        can_delete = True
        for request_step in procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_STEPS]:
            if api_constants.ATTRIBUTE_ID in request_step and request_step[api_constants.ATTRIBUTE_ID] == db_step.id:
                can_delete = False
                break

        if can_delete:
            steps_to_delete.append(db_step)

    for step_to_delete in steps_to_delete:
        procedure_to_update.steps.remove(step_to_delete)
        db.session.delete(step_to_delete)

    for request_step in procedure[api_constants.PROCEDURE_POST_ATTRIBUTE_STEPS]:
        if api_constants.ATTRIBUTE_ID not in request_step:
            step_to_insert = Step(
                name=request_step[api_constants.ATTRIBUTE_NAME],
                type=request_step[api_constants.STEP_POST_ATTRIBUTE_TYPE],
                sequence_number=request_step[api_constants.STEP_POST_ATTRIBUTE_SEQUENCE_NUMBER],
                description=request_step[api_constants.STEP_POST_ATTRIBUTE_DESCRIPTION]
            )
            type_value = request_step[api_constants.STEP_POST_ATTRIBUTE_TYPE]
            if type_value == db_constants.STEP_TYPE_ENUM_VIDEO or type_value == db_constants.STEP_TYPE_ENUM_IMAGE:
                step_to_insert.media_url = request_step[api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL]

            procedure_to_update.steps.append(step_to_insert)
        else:
            for db_step in procedure_to_update.steps:
                if request_step[api_constants.ATTRIBUTE_ID] == db_step.id:
                    db_step.name = request_step[api_constants.ATTRIBUTE_NAME]
                    db_step.type = request_step[api_constants.STEP_POST_ATTRIBUTE_TYPE]
                    db_step.sequence_number = request_step[api_constants.STEP_POST_ATTRIBUTE_SEQUENCE_NUMBER]
                    db_step.description = request_step[api_constants.STEP_POST_ATTRIBUTE_DESCRIPTION]

                    type_value = request_step[api_constants.STEP_POST_ATTRIBUTE_TYPE]
                    if type_value == db_constants.STEP_TYPE_ENUM_TEXT:
                        db_step.media_url = None
                    elif type_value == db_constants.STEP_TYPE_ENUM_VIDEO or type_value == db_constants.STEP_TYPE_ENUM_IMAGE:
                        db_step.media_url = request_step[api_constants.STEP_POST_ATTRIBUTE_MEDIA_URL]

    db.session.commit()
    return True

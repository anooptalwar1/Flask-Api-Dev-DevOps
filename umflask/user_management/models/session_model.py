from user_management import db
from user_management.constants import api_constants
from user_management.constants import db_constants
from user_management.utils import db_utils


class Session(db.Model):
    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    status = db.Column(db.Enum(db_constants.SESSION_STATUS_ENUM_ONLINE,
                               db_constants.SESSION_STATUS_ENUM_OFFLINE,
                               db_constants.SESSION_STATUS_ENUM_BUSY), nullable=False)
    device_type = db.Column(db.Enum(db_constants.SESSION_DEVICE_TYPE_ENUM_HOLOLENS,
                                    db_constants.SESSION_DEVICE_TYPE_ENUM_ANDROID))
    device_ip = db.Column(db.String(20), unique=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    hololens_username = db.Column(db.String(20))
    hololens_password = db.Column(db.String(20))
    session_id = db.Column(db.String(85))


def update_session(user_id, ip_address, session):
    session_to_update = Session.query.filter(
        Session.user_id == user_id).first()
    if not session_to_update:
        return None
    else:
        has_updates = False
        key = api_constants.SESSION_UPDATE_ATTRIBUTE_STATUS
        if key in session:
            value = session[key]
            if session_to_update.status != value:
                if value == db_constants.SESSION_STATUS_ENUM_ONLINE:
                    session_to_update.start_time = db.func.current_timestamp()
                elif value == db_constants.SESSION_STATUS_ENUM_OFFLINE:
                    session_to_update.end_time = db.func.current_timestamp()
                session_to_update.status = value
                has_updates = True

        key = api_constants.SESSION_UPDATE_ATTRIBUTE_DEVICE_TYPE
        if key in session:
            value = session[key]
            if value != session_to_update.device_type:
                session_to_update.device_type = value
                has_updates = True

        if ip_address != session_to_update.device_ip:
            session_to_update.device_ip = ip_address
            has_updates = True

        if session_to_update.device_type == db_constants.SESSION_DEVICE_TYPE_ENUM_HOLOLENS:
            key = api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_USERNAME
            if key in session:
                value = session[key]
                if value != session_to_update.hololens_username:
                    session_to_update.hololens_username = value
                    has_updates = True

            key = api_constants.SESSION_UPDATE_ATTRIBUTE_HOLOLENS_PASSWORD
            if key in session:
                value = session[key]
                if value != session_to_update.hololens_password:
                    session_to_update.hololens_password = value
                    has_updates = True

        if has_updates:
            db.session.commit()
            return session_to_update.device_type
        else:
            return False


def set_status_offline(ip_address):
    session_to_update = Session.query.filter(
        Session.device_ip == ip_address).first()
    if not session_to_update:
        return None
    else:
        session_to_update.status = db_constants.SESSION_STATUS_ENUM_OFFLINE
        db.session.commit()
        return session_to_update.device_type


def get_online_hololens_users():
    query = "SELECT * FROM online_hololens_users_view"
    rows = db.engine.execute(query).fetchall()
    if len(rows) == 0:
        return []
    else:
        return db_utils.convert_rows_to_dictionary(rows)

def get_online_android_users():
    query = "SELECT * FROM online_android_users_view"
    rows = db.engine.execute(query).fetchall()
    if len(rows) == 0:
        return []
    else:
        return db_utils.convert_rows_to_dictionary(rows)

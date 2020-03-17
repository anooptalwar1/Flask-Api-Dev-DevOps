from user_management import db
from user_management import ma
from user_management.constants import api_constants
from user_management.constants import db_constants
from user_management.utils import db_utils


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    level = db.Column(db.Enum(db_constants.USER_LEVEL_ENUM_ADMIN,
                              db_constants.USER_LEVEL_ENUM_TECH_SUPPORT,
                              db_constants.USER_LEVEL_ENUM_REMOTE_OPERATOR,
                              db_constants.USER_LEVEL_ENUM_READ_ONLY), nullable=False,
                      default=db_constants.USER_LEVEL_ENUM_READ_ONLY)
    is_deactive = db.Column(db.Integer, nullable=False, default=0)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session


ALL_PUBLIC_COLUMNS_ARRAY = ['id', 'name', 'email', 'level']


def get_all_users_for_user_id(user_id):
    user = User.query.filter(
        db.and_(User.id == user_id, User.is_deactive == 0)).first()
    if not user:
        return None
    else:
        query = "SELECT * FROM users_for_dashboard_view WHERE id <> {}".format(
            user_id)

        rows = db.engine.execute(query).fetchall()
        if len(rows) == 0:
            return 0
        else:
            return db_utils.convert_rows_to_dictionary(rows)


def insert_user(user):
    user_to_insert = User(
        name=user[api_constants.USER_POST_ATTRIBUTE_NAME],
        email=user[api_constants.USER_POST_ATTRIBUTE_EMAIL],
        password=user[api_constants.USER_POST_ATTRIBUTE_PASSWORD]
    )

    key = api_constants.USER_POST_ATTRIBUTE_LEVEL
    if key in user:
        user_to_insert.level = user[key]

    db.session.add(user_to_insert)
    try:
        db.session.commit()
    except Exception as ex:
        return ex
    else:
        user_schema = UserSchema(only=ALL_PUBLIC_COLUMNS_ARRAY)
        return user_schema.dump(user_to_insert)


def check_login_credentials(credentials):
    user = User.query.filter(db.and_(User.email == credentials[api_constants.USER_POST_ATTRIBUTE_EMAIL]),
                             (User.password ==
                              credentials[api_constants.USER_POST_ATTRIBUTE_PASSWORD]),
                             (User.is_deactive == 0)).first()
    if not user:
        return None
    else:
        users_schema = UserSchema(only=ALL_PUBLIC_COLUMNS_ARRAY)
        return users_schema.dump(user)


def update_user(user, user_id):
    calling_user = User.query.filter(
        db.and_(User.id == user_id), (User.is_deactive == 0)).first()
    if not calling_user:
        return None
    else:
        updating_another_user = False
        key = api_constants.ATTRIBUTE_ID
        if key in user:
            value = user[key]
            user_to_update = User.query.filter(
                db.and_(User.id == value), (User.is_deactive == 0)).first()
            updating_another_user = True
            if not user_to_update:
                return value
        else:
            user_to_update = calling_user

        if updating_another_user:
            if calling_user.level != db_constants.USER_LEVEL_ENUM_ADMIN:
                return None
        else:
            old_password_key = api_constants.USER_POST_ATTRIBUTE_OLD_PASSWORD
            password_key = api_constants.USER_POST_ATTRIBUTE_PASSWORD
            if old_password_key in user and password_key in user:
                if user_to_update.password != user[old_password_key]:
                    return False
                else:
                    user_to_update.password = user[password_key]

        key = api_constants.USER_POST_ATTRIBUTE_NAME
        if key in user:
            user_to_update.name = user[key]

        db.session.commit()
        users_schema = UserSchema(only=ALL_PUBLIC_COLUMNS_ARRAY)
        return users_schema.dump(user_to_update)


def deactivate_user(user_id, user):
    calling_user = User.query.filter(User.id == user_id).first()
    if not calling_user or calling_user.is_deactive == 1 or calling_user.level != db_constants.USER_LEVEL_ENUM_ADMIN:
        return False
    else:
        user_to_update = User.query.filter(
            User.id == user[api_constants.ATTRIBUTE_ID]).first()
        if not user_to_update:
            return user[api_constants.ATTRIBUTE_ID]
        else:
            user_to_update.is_deactive = 1
            db.session.commit()
            return True

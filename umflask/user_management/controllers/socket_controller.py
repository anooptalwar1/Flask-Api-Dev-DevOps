from user_management.controllers import session_controller


def update_session(ip_address, json_data):
    return session_controller.update_session(ip_address, json_data)


def get_online_hololens_users():
    return session_controller.get_online_hololens_users()


def get_online_android_users():
    return session_controller.get_online_android_users()


def set_status_offline(ip_address):
    return session_controller.set_status_offline(ip_address)

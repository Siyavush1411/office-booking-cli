CURRENT_USER = 0


def save_current_user_to_session(user_id):
    global CURRENT_USER
    CURRENT_USER = user_id


def get_current_user_from_session():
    return CURRENT_USER
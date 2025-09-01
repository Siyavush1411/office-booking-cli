from models.user import User


class UserService:
    def get_user_by_username(self, username: str) -> User | None:
        user = User.get(field="username", value=username)
        if user:
            return user
        return None

class UserConfirmations:
    def _confirm_email(self):
        email = input("Введите email: ")
        confirm_email = input(
            f"Вы уверены, что хотите использовать этот email {email}? подтвердите пожалуйста ваш email: "
            )
        if email != confirm_email:
            print("Email не совпадает. Попробуйте еще раз.")
            return self._confirm_email()
        return email

    def _confirm_password(self):
        password = input("Введите пароль: ")
        confirm_password = input("Подтвердите пароль: ")
        if password != confirm_password:
            print("Пароли не совпадают. Попробуйте еще раз.")
            return self._confirm_password()
        return password

    def _confirm_phone(self):
        phone = input("Введите номер телефона: ")
        confirm_phone = input("Подтвердите номер телефона: ")
        if phone != confirm_phone:
            print("Номера не совпадают. Попробуйте еще раз.")
            return self._confirm_phone()
        return phone

#!/usr/bin/env python3
'''User module'''
import hashlib
from models.base import Base


class AlreadyExists(Exception):
    '''Raised if the user already exists'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DoesNotExist(Exception):
    '''Raised if the user doesn't exist'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class User(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self._email = kwargs.get('_email')
        self._password = kwargs.get('_password')
        self.role = None
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.session_id = None
        self.reset_token = None

    @property
    def email(self) -> str:
        '''Getter of the email'''
        return self._email

    @email.setter
    def email(self, email: str):
        '''Setter of new email'''
        if len(User.search({'email': email})) > 0:
            raise AlreadyExists('This email is already in use')
        else:
            self._email = email

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

if __name__ == '__main__':
    User.load_from_file()

    user_email = "bob@hbtn.io"
    user_clear_pwd = "H0lbertonSchool98!"

    user = User(first_name='Mark', last_name='The Zuck')
    user.email = user_email
    user.password = user_clear_pwd
    print("New user: {}".format(user.id))
    print('Display name: {}'.format(user.display_name()))
    print('Hashed password: {}\n'.format(user.password))
    print(user.to_json())
    print(user.__dict__)
    # user.save()

    # user_email = "braap@bop.mid"
    # user_clear_pwd = "H0ltryuhiop98!"

    # user = User(first_name='Tim', last_name='Cuck')
    # user.email = user_email
    # user.password = user_clear_pwd
    # print("New user: {}".format(user.id))
    # print('Display name: {}'.format(user.display_name()))
    # print('Hashed password: {}\n'.format(user.password))

    # print(user.to_json())

    # user.save()
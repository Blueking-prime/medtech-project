#!/usr/bin/env python3
'''Contains the user data modification functions'''
from uuid import uuid4
from models.user import User, DoesNotExist


class UserData:
    '''User class to handle user data modification'''

    @classmethod
    def register_user(cls, email: str, password: str, name: tuple) -> User:
        '''Registers a new user'''
        user = User()
        user.email = email
        user.password = password
        user.first_name = name[0]
        user.last_name = name[1]
        user.save()
        return user

    @classmethod
    def update_data(cls, user: User, **kwargs) -> None:
        '''Updates a users general data'''
        for i in kwargs.keys():
            user.__setattr__(i, kwargs.get(i))

        user.save()

    @classmethod
    def update_email(cls, user: User, email: str, password: str) -> bool:
        '''Updates a users email'''
        if user.is_valid_password(password):
            user.email = email
            user.save()
            return True
        else:
            return False

    @classmethod
    def update_password(cls, reset_token: str, password: str) -> None:
        '''Updates a users password'''
        try:
            user: User = User.search({'reset_token': reset_token})[0]
            user.password = password
            user.save()
            UserData.update_data(user, reset_token=None)
        except IndexError:
            raise DoesNotExist('Can\'t find the user with this reset token')

    @classmethod
    def get_reset_password_token(cls, email: str) -> str:
        '''Gets a user's reset token'''
        try:
            user = User.search({'email': email})[0]
            token = str(uuid4())
            UserData.update_data(user, reset_token=token)
            return token
        except IndexError:
            raise DoesNotExist(f'Can\'t find the user with email: {email}')

#!/usr/bin/env python3
'''Contains the authentication functions'''
from uuid import uuid4
from api.v1.auth.user import UserData, User, DoesNotExist


class Auth:
    '''Auth class to handle user authentication'''

    def __init__(self):
        pass

    # Authentication stuff
    def valid_login(self, email: str, password: str) -> bool:
        '''Try to log in the user'''
        try:
            user : User = User.search({'_email':email})[0]
            print(user, email)
            return user.is_valid_password(password)
        except IndexError:
            raise DoesNotExist(f'Can\'t find the user with email: {email}')

    # Session Shenanigins
    def create_session(self, email: str) -> str | None:
        '''returns the session id for a given email'''
        try:
            user: User = User.search({'email': email})[0]
            UserData.update_data(user, session_id=str(uuid4()))
            return user.session_id
        except IndexError:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        '''Returns a user with the session id'''
        if session_id is None:
            return None
        try:
            user: User = User.search({'session_id': session_id})[0]
            return user
        except IndexError:
            return None

    def destroy_session(self, user_id: str) -> None:
        '''Destroys a user's session'''
        try:
            user: User = User.search({'id': user_id})[0]
            UserData.update_data(user, session_id=None)
        except IndexError:
            raise DoesNotExist(f'Can\'t find the user with id: {user_id}')


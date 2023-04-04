#!/usr/bin/env python3
'''Contains the authentication functions'''
from uuid import uuid4
from api.v1.auth.user_data import UserData, User, DoesNotExist


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

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        return request.cookies.get('session_id')

    def authorization_header(self, request=None) -> str:
        '''The authorization header for the request'''
        if request.headers.get('Authorization'):
            return request.headers.get('Authorization')
        return None

    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        '''Determine if user requires auth'''
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path not in excluded_paths and path + '/' not in excluded_paths:
            return True
        else:
            return False

#!/usr/bin/env python3
'''Module of auth routes'''
from flask import jsonify, abort, request
from api.v1.auth.auth import Auth
from api.v1.views import app_views, UserData
from api.v1.views.index import status


AUTH = Auth()

@app_views.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> tuple[str, int]:
    """ POST /sessions

    Creates a login session

    Return:
      - the login response
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email, password)
    validity = AUTH.valid_login(email, password)
    if validity:
        session_id = AUTH.create_session(email)
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie("session_id", session_id)
        return out, 200
    else:
        abort(401)


@app_views.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> tuple[str, int]:
    """ DELETE /sessions

    Deletes a login session

    Return:
      - the login response
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return status()
    else:
        abort(403)


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> tuple[str, int]:
    """ POST /reset_password

    Creates a password reset token

    Return:
      - the reset token
    """
    data = request.form
    email = data.get('email')
    try:
        token = UserData.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> tuple[str, int]:
    """ PUT /reset_password

    Changes a user's password

    Return:
      - success message
    """
    data = request.form
    email = data.get('email')
    token = data.get('reset_token')
    new_password = data.get('new_password')
    try:
        UserData.update_password(token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)

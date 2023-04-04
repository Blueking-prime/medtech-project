#!/usr/bin/env python3
'''Module of auth routes'''
from flask import jsonify, abort, request
from api.v1.auth.user_data import User
from api.v1.views import app_views


@app_views.route('/meds/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_users_meds(user_id: str = None) -> str:
    """ GET /api/v1/meds/:id
    Path parameter:
      - User ID
    Return:
      - User object meds JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        try:
            user = request.current_user
        except AttributeError:
            user = None
    else:
        user: User = User.get(user_id)

    if user is None:
        abort(404)
    if user.medication is None:
        abort(404)
    return jsonify(user.to_json().get('medication'))


@app_views.route('/meds/<user_id>/<drug_name>', methods=['DELETE'], strict_slashes=False)
def delete_user_meds(user_id: str = None, drug_name: str = None) -> str:
    """ DELETE /api/v1/meds/:id/:drug_name
    Path parameter:
      - User ID
      - Drug Name
    JSON Body:
      - Password
    Return:
      - empty JSON is the drug has been correctly deleted
      - 400 if password or drug name not supplied
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        try:
            user = request.current_user
        except AttributeError:
            user = None
    else:
        user: User = User.get(user_id)

    if user is None:
        abort(404)
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    if rj is None:
        error_msg = "Wrong format"
    password = rj.get("password")
    if error_msg is None and drug_name is None:
        error_msg = "no drug specified"
    if error_msg is None and password == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user.remove_medication(drug_name, password)
            return jsonify({}), 200
        except Exception as e:
            error_msg = "Can't delete drug: {}".format(e)
    return jsonify({'error': error_msg}), 400



@app_views.route('/meds/<user_id>', methods=['POST', 'PUT'], strict_slashes=False)
def create_or_update_med_entry(user_id: str = None) -> str:
    """ POST or PUT /api/v1/users/
    JSON body:
      - password
      - med_data ie. {
                'drug_name': [
                    'dose',
                    'time between doses (hours)',
                    'max total doses [optional]',
                    'date medication was issued [optional]
                ],
            }
    Return:
      - User medications JSON represented
      - 400 if can't create the new medication
      - 404 if user not found
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        try:
            user = request.current_user
        except AttributeError:
            user = None
    else:
        user: User = User.get(user_id)

    if user is None:
        abort(404)

    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    if rj is None:
        error_msg = "Wrong format"
    med_data = rj.get("med_data")
    password = rj.get("password")
    if error_msg is None and med_data == "":
        error_msg = "med_data missing"
    if error_msg is None and password == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user.update_medication(med_data, password)
            return jsonify(user.to_json().get('medication')), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400

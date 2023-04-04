#!/usr/bin/env python3
'''Module of basic api routes'''
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/info', methods=['GET'], strict_slashes=False)
def info() -> str:
    """ GET /api/v1/info
    Return:
      - Help about the API
    """

    routes = '''
    ----------BASIC API ROUTES----------

    GET /api/v1/status
        Checks the status of the API

        Return:
        - the status of the API

    GET /api/v1/info
        Shows info about the API including valid routes

        Return:
        - Help about the API

    ----------LOGIN ROUTES----------

    POST /sessions
        Creates a login session

        Return:
        - the login response

    DELETE /sessions
        Deletes a login session

        Return:
        - the login response

    POST /api/v1/users/new
        Creates a new user

        JSON body:
            - email
            - password
            - last_name (optional)
            - first_name (optional)
        Return:
            - User object JSON represented
            - 400 if can't create the new User

    ----------USERS ROUTES----------

    PUT /api/v1/users/:id
        Updates an existing user

        Path parameter:
        - User ID
        JSON body:
        - last_name (optional)
        - first_name (optional)
        Return:
        - User object JSON represented
        - 404 if the User ID doesn't exist
        - 400 if can't update the User

    DELETE /api/v1/users/:id
        Deletes a user

        Path parameter:
        - User ID
        Return:
        - empty JSON is the User has been correctly deleted
        - 404 if the User ID doesn't exist

    GET /api/v1/users
        Gets all the users' data

        Return:
        - list of all User objects JSON represented

    GET /api/v1/users/:id
        View a user's data

        Path parameter:
        - User ID
        Return:
        - User object JSON represented
        - 404 if the User ID doesn't exist

    POST /reset_password
        Creates a password reset token

        Return:
        - the reset token

    PUT /reset_password
        Changes a user's password

        Return:
        - success message

    ----------MEDICATION ROUTES----------

    GET /api/v1/meds/:id
        View one user's meds

        Path parameter:
        - User ID
        Return:
        - User object meds JSON represented
        - 404 if the User ID doesn't exist

    POST or PUT /api/v1/users/
        Add a users meds

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

    DELETE /api/v1/meds/:id/:drug_name
        Deletes a users medication

        Path parameter:
        - User ID
        - Drug Name
        JSON Body:
        - Password
        Return:
        - empty JSON is the drug has been correctly deleted
        - 400 if password or drug name not supplied
        - 404 if the User ID doesn't exist
    '''
    return routes

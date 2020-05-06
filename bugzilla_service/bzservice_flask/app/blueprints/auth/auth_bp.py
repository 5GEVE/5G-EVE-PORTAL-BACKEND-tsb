from flask import ( Blueprint, jsonify, request )
from app import db, bcrypt, bz_client, kc_client

import requests

from app.models.user import *

from app.keycloak.keycloak_client import Keycloak
from app.bugzilla.bugzilla_client import BugzillaClient

# BLUEPRINT CREATION
bp = Blueprint('auth', __name__, url_prefix='')

# ROUTES DEFINITION
@bp.route('/register', methods=['POST'])
def registration():
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"details": "Json not correctly formatted"}), 400
    
    schema = BugzillaUserSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"details": errors}), 400

    # check uniqueness of the username and email in local database
    if not BugzillaUser.query.filter_by(email=data['email']).first() == None:
        return jsonify({"details": "Username already registered"}), 400

    # Create user in bugzilla
    status, msg = bz_client.create_user(data)
    if status in [200, 201]:
        # Hash password
        data['password'] = bcrypt.generate_password_hash(data['password'].encode('utf-8'))
        
        # Store new user in local database
        new_user = schema.load(data)
        db.session.add(new_user)
        db.session.commit()

    return jsonify({'details': msg}), status



@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()
    if 'email' not in data.keys() or 'password' not in data.keys():
        return jsonify({"details": "Email or password not provided"}), 400
        
    status, msg = bz_client.login(data)
    
    if status == requests.codes.ok:
        user = BugzillaUser.query.filter_by(email=data['email']).first()
        if user:
            # Request user details and store bugzilla user id
            #TODO: lo ideal es guardar el user_id de keycloak cuando se registre
            #token_to_user_status, token_to_user_msg = kc_client.token_to_user(msg['token'])
            #if token_to_user_status == requests.codes.ok:
                #user.bz_user_id = token_to_user_msg['id']
            user.apikey = msg['token']
            db.session.commit()

            return jsonify({"details": "User correctly logged in", "token": msg['token']}), 200

        else:
            schema = BugzillaUserSchema()

            data['password'] = bcrypt.generate_password_hash(data['password'].encode('utf-8'))
            data['apikey'] = msg['token']
            data['full_name'] = data['email']

            # Store user in local database
            new_user = schema.load(data)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"details": "User correctly logged in", "token": msg['token']}), 200

        print("[AUTH_BP][ERROR] > User correctly logged in at bugzilla but not found at local database")
        return jsonify({"details": "Internal server error"}), 500
    
    return jsonify({"details": msg}), status

#TODO: oidc
@bp.route('/logout', methods=['GET'])
def logout():
    token = str(request.headers['authorization']).split(" ")[1]
    user_email = kc_client.get_user_email(token)
    
    user = BugzillaUser.query.filter_by(email=user_email).first()

    if user:
        status, msg = bz_client.logout(user.apikey)

        if status == requests.codes.ok:
            user.apikey = ""
            db.session.commit()

            return jsonify({"details": "User session corretly closed"}), 200

        return jsonify({"details": msg}), status
    else:
        print("[AUTH_BP][ERROR] > User correctly logged in at keycloak but not found at local database")
        return jsonify({"details": "Internal server error"}), 500


@bp.route('/changepassword', methods=['PUT'])
def change_password():
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    token = str(request.headers['authorization']).split(" ")[1]

    try:
        new_password = data['new_password']
    except KeyError as error:
        return jsonify({"details": "Parameter {} not provided".format(error)}), 400

    user_email = kc_client.get_user_email(token)
    
    user = BugzillaUser.query.filter_by(email=user_email).first()

    if user:
        status, msg = bz_client.change_password(user_email, new_password)

        if status == requests.codes.ok:
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"details": "Password correctly updated"}), status

        return jsonify({"details": msg}), status

    else:
        print("[AUTH_BP][ERROR] > User correctly logged in at keycloak but not found at local database")
        return jsonify({"details": "Internal server error"}), 500
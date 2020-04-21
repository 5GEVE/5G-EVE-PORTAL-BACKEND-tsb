from flask import ( Blueprint, jsonify, request )
from app import db, bcrypt, oidc, bz_client, kc_client
import json, requests
from datetime import datetime
from app.models.user import *

# BLUEPRINT CREATION
bp = Blueprint('bugs', __name__, url_prefix='/portal/tsb/tickets')

#### ROUTES DEFINITION ####
# ?page=10
@bp.route('', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_bugs():
    page = int(request.args.get('page'))
    
    token = str(request.headers['authorization']).split(" ")[1]
    status_code, msg = kc_client.token_to_user(token)

    if status_code == requests.codes.ok:
        user = BugzillaUser.query.filter_by(email=msg['email']).first()
        if user: 
            bugzilla_token = user.apikey
            #TODO: admin roles
            msg['roles'] = "ADMIN"
            if "ADMIN" in msg['roles']:
                status, msg = bz_client.get_bugs(requester_email=msg['email'], requester_token=bugzilla_token, is_admin=True, page=page)
            else:
                status, msg = bz_client.get_bugs(requester_email=msg['email'], requester_token=bugzilla_token, is_admin=False, page=page)
            
            return jsonify({'details': msg}), status
            #if status != requests.codes.ok:
            #    return jsonify({'details': msg}), status
            #else:
                #sorted_data = sorted(msg['bugs'], key=lambda k: datetime.strptime(k['creation_time'],'%Y-%m-%dT%H:%M:%SZ'), reverse=False)
                #return jsonify({'details': sorted_data}), status

        else:
            print("SERVER > [ERROR] user {} not found in the DB but correctly logged in at Keycloak".format(msg['email']))
            return jsonify({'details': 'Internal server error'}), 500
    
    return msg, status_code

@bp.route('/<bug_id>', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_bug(bug_id):
    token = str(request.headers['authorization']).split(" ")[1]
    status_code, msg = kc_client.token_to_user(token)
    if status_code == requests.codes.ok:
        user = BugzillaUser.query.filter_by(email=msg['email']).first()
        if user:
            bugzilla_token = user.apikey
            #TODO: admin roles
            msg['roles'] = "ADMIN"
            if "ADMIN" in msg['roles']:
                status, msg = bz_client.get_bug(requester_email=msg['email'], requester_token=bugzilla_token, bug_id=bug_id, is_admin=True)
            else:
                status, msg = bz_client.get_bug(requester_email=msg['email'], requester_token=bugzilla_token, bug_id=bug_id, is_admin=False)
            return jsonify({'details': msg}), status

        else:
            print("SERVER > [ERROR] user {} not found in the DB but correctly logged in at Keycloak")
            return jsonify({'details': 'Internal server error'}), 500
    else:
        return msg, status_code


@bp.route('', methods=['POST'])
@oidc.accept_token(require_token=True)
def create_bug():
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    token = str(request.headers['authorization']).split(" ")[1]
    status_code, msg = kc_client.token_to_user(token)

    if status_code != requests.codes.ok:
        return msg, status_code

    else:
        user = BugzillaUser.query.filter_by(email=msg['email']).first()
        if user:
            bugzilla_token = user.apikey

            #TODO: check user roles that are able to create bugs
            msg['roles'] = 'USER_ALLOWED'
            if "USER_ALLOWED" in msg['roles']:
                status, msg = bz_client.create_bug(reporter_token=bugzilla_token, bug_data=data)
                return jsonify({'details': msg}), status
                
            else:
                return jsonify({'details': 'User not allowed to create bugs'}), 401
        else:
            print("SERVER > [ERROR] user {} not found in the DB but correctly logged in at Keycloak")
            return jsonify({'details': 'Internal server error'}), 500

@bp.route('/<bug_id>', methods=['POST'])
@oidc.accept_token(require_token=True)
def update_bug(bug_id):
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    token = str(request.headers['authorization']).split(" ")[1]
    user_data = kc_client.token_to_user(token)

    user = BugzillaUser.query.filter_by(email=user_data['email']).first()
    
    if user:
        bugzilla_token = user.apiKey
        #TODO: Usuario admin tambien tiene que ser admin en Bugzilla
        if "ADMIN" in user_data['roles']:
            status, msg = bz_client.update_bug(reporter_email=user_data['email'] ,reporter_token=bugzilla_token, bug_data=data, bug_id=bug_id, is_admin=True)
        else:
            status, msg = bz_client.update_bug(reporter_email=user_data['email'], reporter_token=bugzilla_token, bug_data=data, bug_id=bug_id, is_admin=False)

    return jsonify({'details': msg}), status 

@bp.route('/<bug_id>/comments', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_bug_comments(bug_id):
    
    token = str(request.headers['authorization']).split(" ")[1]
    status_code, msg = kc_client.token_to_user(token)
    if status_code == requests.codes.ok:

        user = BugzillaUser.query.filter_by(email=msg['email']).first()
        if user:
            bugzilla_token = user.apikey
            #TODO: admin roles
            #print(msg['roles'])
            #msg['roles'] = "ADMIN"
            if "5geve_admin" in msg['roles']:
                status, msg = bz_client.get_bug_comments(requester_token=bugzilla_token, bug_id=bug_id, is_admin=True)
            else:
                status, msg = bz_client.get_bug_comments(requester_token=bugzilla_token, bug_id=bug_id, is_admin=False)
            return jsonify({'details': msg}), status

        else:
            print("SERVER > [ERROR] user {} not found in the DB but correctly logged in at Keycloak")
            return jsonify({'details': 'Internal server error'}), 500
    else:
        return msg, status_code

@bp.route('/<bug_id>/comments', methods=['POST'])
@oidc.accept_token(require_token=True)
def create_bug_comment(bug_id):
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    token = str(request.headers['authorization']).split(" ")[1]
    status_code, msg = kc_client.token_to_user(token)

    if status_code != requests.codes.ok:
        return msg, status_code

    else:
        user = BugzillaUser.query.filter_by(email=msg['email']).first()
        if user:
            bugzilla_token = user.apikey

            #TODO: check user roles that are able to create bugs
            msg['roles'] = 'USER_ALLOWED'
            if "USER_ALLOWED" in msg['roles']:
                status, msg = bz_client.create_bug_comment(user_token=bugzilla_token, bug_id=bug_id, comment_data=data)
                return jsonify({'details': msg}), status
                
            else:
                return jsonify({'details': 'User not allowed to create bugs'}), 401
        else:
            print("SERVER > [ERROR] user {} not found in the DB but correctly logged in at Keycloak")
            return jsonify({'details': 'Internal server error'}), 500

#### TRUSTED ENDPOINTS FOR ELM

#TODO: filter incomming requests. Only requests from ELM are allowed
@bp.route('/trusted', methods=['POST'])
def create_bug_trusted():
    '''
        Allow creation of tickets from the ELM on behalf of an authenticated user
    '''
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    user = BugzillaUser.query.filter_by(email=data['reporter']).first()
    if user:
        bugzilla_token = user.apikey
        status, msg = bz_client.create_bug(reporter_token=bugzilla_token, bug_data=data)

        return jsonify({'details': msg}), status

    else:
        print("SERVER > [ERROR] reporter {} not found", data['reporter'])
        return jsonify({'details': 'User requesting comment creation not found'}), 404

#TODO: filter incomming requests. Only requests from ELM are allowed
@bp.route('/<bug_id>/comments/trusted', methods=['POST'])
def create_bug_comment_trusted(bug_id):
    if not request.is_json:
        return jsonify({"details": "No json provided"}), 400

    data = request.get_json()

    user = BugzillaUser.query.filter_by(email=data['reporter']).first()
    if user:
        bugzilla_token = user.apikey
        status, msg = bz_client.create_bug_comment(user_token=bugzilla_token, bug_id=bug_id, comment_data=data)
        return jsonify({'details': msg}), status

    else:
        print("SERVER > [ERROR] reporter {} not found", data['reporter'])
        return jsonify({'details': 'User requesting comment creation not found'}), 404

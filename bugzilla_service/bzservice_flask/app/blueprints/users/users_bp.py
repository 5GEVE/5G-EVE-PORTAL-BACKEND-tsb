from flask import ( Blueprint, jsonify, request )
from app import db, bcrypt, oidc, bz_client, kc_client
import json
from app.models.user import *

# BLUEPRINT CREATION
bp = Blueprint('users', __name__, url_prefix='/portal/tsb/adminusers')

#### ROUTES DEFINITION ####
@bp.route('', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_users():
    
    status, msg = bz_client.get_admin_users()
    
    return jsonify({"details": msg}), status

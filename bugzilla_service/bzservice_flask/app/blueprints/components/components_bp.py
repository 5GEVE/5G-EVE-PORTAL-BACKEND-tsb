from flask import ( Blueprint, jsonify, request )
from app import db, bcrypt, oidc, bz_client, kc_client
import json
from app.models.user import *

# BLUEPRINT CREATION
bp = Blueprint('components', __name__, url_prefix='/components')

#### ROUTES DEFINITION ####
#/components?product_id=1
@bp.route('', methods=['GET'])
@oidc.accept_token(require_token=True)
def get_components():
    """ If we include detailed=true as a query parameter, we will obtain a more details about the component
    """
    product_id = request.args.get('product_id')
    detailed = request.args.get('detailed')
    
    status, msg = bz_client.get_components(product_id, detailed)
    
    return jsonify({"details": msg}), status
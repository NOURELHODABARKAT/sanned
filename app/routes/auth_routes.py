# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController

import logging

logging.basicConfig(level=logging.INFO)

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
 
    data = request.get_json()
    ip_address = request.remote_addr if hasattr(request, 'remote_addr') else None
    response, status = AuthController.sign_up(data, ip_address)
    return jsonify(response), status

@auth_bp.route('/users/<int:user_id>/username', methods=['PUT'])
def update_username(user_id):
    data = request.get_json()
    response, status = AuthController.update_username(user_id, data)
    return jsonify(response), status

@auth_bp.route('/users/<int:user_id>/skills', methods=['GET'])
def get_user_skills(user_id):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    response = AuthController.get_user_skills(user_id, limit, offset)
    return jsonify(response)
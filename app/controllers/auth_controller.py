# app/controllers/auth_controller.py
from flask import jsonify
from app.models import User, UserSkill
from app.services.location_service import LocationService
from app.services.username_services import UsernameService
from app.services.security_service import SecurityService
from app.utils.schema_validator import SchemaValidator
from app import db
import logging

logging.basicConfig(level=logging.INFO)

class AuthController:
    @staticmethod
    def sign_up(data, ip_address=None):
        validated_data = SchemaValidator.validate_user(data)
        location_service = LocationService()
        
       
        location_data = location_service.get_ip_location(ip_address) if ip_address else None
        
     
        location_data = location_data or location_service.get_manual_location(validated_data['city'])
        if not location_data:
            raise ValueError("Unable to determine location")
        
     
        username = validated_data.get('username') or UsernameService.generate_unique_username(
            validated_data['email']
        )
        

        password_hash = SecurityService.hash_password(validated_data['password'])
        
        user = User(
            username=username,
            email=validated_data['email'],
            password_hash=password_hash,
            role=validated_data['role'],
            phone=validated_data.get('phone'),
            location=f"{location_data['city']}, {location_data['country']}" if location_data and location_data.get('city') and location_data.get('country') else location_data.get('city'),
            latitude=location_data.get('latitude'),
            longitude=location_data.get('longitude'),
            is_in_gaza=location_data.get('is_in_gaza', False)
        )
        db.session.add(user)
        db.session.commit()
        
      
        token = SecurityService.generate_token(user.id)
        
        response = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'location': user.location,
            'is_in_gaza': user.is_in_gaza,
            'token': token
        }
        logging.info(f"User registered: {response}")
        return response, 201

    @staticmethod
    def update_username(user_id, data):
        validated_data = SchemaValidator.validate_username_update(data)
        new_username = UsernameService.update_username(user_id, validated_data['username'])
        response = {'username': new_username}
        logging.info(f"Username updated for user_id {user_id}: {response}")
        return response, 200

    @staticmethod
    def get_user_skills(user_id, limit=10, offset=0):
        user = User.query.get_or_404(user_id)
        skills = user.skills.offset(offset).limit(limit).all()
        total = user.skills.count()
        
        response = {
            'skills': [{'id': s.id, 'skill': s.skill} for s in skills],
            'total': total,
            'limit': limit,
            'offset': offset,
            'next': f"/api/users/{user_id}/skills?limit={limit}&offset={offset + limit}" if offset + limit < total else None
        }
        logging.info(f"Skills retrieved for user_id {user_id}: {response}")
        return response
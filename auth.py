from flask import Blueprint, jsonify, request
from models import TokenBlocklist, User
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required, 
                                get_jwt,
                                current_user,
                                get_jwt_identity)
auth_bp = Blueprint("auth", __name__,)

@auth_bp.post('/register')
def register_user():
    
    data = request.get_json()
    user=User.get_user_by_username(username=data['username'])
    if user is not None:
        return jsonify({"message":"username already exists"}) ,409
    new_user = User(
        username=data['username'],
        email=data['email']
        )
    new_user.set_password(data.get('password'))
    new_user.save()

    return jsonify({"message":"user registered successfully"}),201

@auth_bp.post('/login')
def login_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    if user and (user.check_password(password=data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify(
            {
                "message":"user logged in successfully",
                "token":{
                    "access_token":access_token,
                    "refresh_token":refresh_token
                }

            }
            
            ),201

    return jsonify({"error":"invalid username or password"}),401

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
  
    return jsonify({"message":"you are authenticated",
                    "user_details": {"username":current_user.username,
                    "email":current_user.email}}),200

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token})

@auth_bp.get('/logout')
@jwt_required()
def logout_user():
    jwt = get_jwt()
    jti = jwt["jti"]
    token_type = jwt["type"]
    token_b = TokenBlocklist(jti=jti)
    token_b.save()
    return jsonify({"message":f"{token_type} token revoked successfully"}),200
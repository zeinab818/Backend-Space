from flask import Flask,jsonify
from dotenv import load_dotenv
from extensions import db ,jwt
from auth import auth_bp
from users import users_bp
from models import TokenBlocklist, User
from exploration import exploration_bp
from extensions import db, jwt, migrate
load_dotenv() 

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(
    exploration_bp,
    url_prefix="/api/exploration"
)


    # look up loader
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()
    
    
    # addtional claims
    
    def make_additional_claims(identity):
        if identity == "staff123":
            return {"is_staff": True}
        return {"is_staff": False}

    # errors handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has expired.",
            "error": "token_expired"
        }), 401
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Signature verification failed.",
            "error": "invalid_token"
        }), 401
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_data):

        jti = jwt_data["jti"]
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti==jti).scalar()
        
        return token is not None
    
    
    

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
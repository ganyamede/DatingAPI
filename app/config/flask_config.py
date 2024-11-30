import os
from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from app.endpoints.routes import App
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger

#Flask
app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

#SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#JWT
app.config["JWT_SECRET_KEY"] = "..."
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Срок действия access токена
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

#Route

app.register_blueprint(App, url_prefix='/api')
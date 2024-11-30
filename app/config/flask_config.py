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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://getapple:010203@localhost/getapple'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#JWT
app.config["JWT_SECRET_KEY"] = "64459822c292d8aee8da650590c9859cea0d1bfda97f1a31a928f787ae2666ae"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Срок действия access токена
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

#Route

app.register_blueprint(App, url_prefix='/api')
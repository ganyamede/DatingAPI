from flask import request
from flask_restful import Resource
from app.security.user_encryption import hash_password, verify_password
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

class AuthorizationBase:
    def validate_inputs(self, gmail, password):
        if not gmail or not password:
            raise ValueError("Provide 'gmail' and 'password'")
        if '@' not in gmail:
            raise ValueError("Email entered incorrectly")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

    def get_user_by_email(self, gmail):
        # Deferred import to avoid circular import
        from app.database import Users

        return Users.query.filter_by(gmail=gmail).first()

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        API to get a new access token using the refresh token
        ---
        tags:
            - Auth
        responses:
         200:
           description: New access token
           schema:
             type: object
             properties:
               ok:
                 type: boolean
                 example: true
               state:
                 type: boolean
                 example: true
               access_token:
                 type: string
                 example: "new-access-token"
        """
        current_gmail = get_jwt_identity()
        new_access_token = create_access_token(identity=current_gmail)
        return {'ok': True,  'state': True, "access_token": new_access_token}, 200

class Register(AuthorizationBase, Resource):
    def post(self):
        """
        API for registering a new user
        ---
        tags:
            - Auth
        parameters:
          - name: gmail
            in: body
            type: string
            required: true
            description: User's email address
          - name: password
            in: body
            type: string
            required: true
            description: User's password
        responses:
          200:
            description: Successful registration
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
                user_id:
                  type: integer
                  example: 123
                message:
                  type: string
                  example: "Account successfully created"
          400:
            description: Validation error of input data
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Invalid email or password"
          409:
            description: User already exists
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "User already exists"
        """

        from app.database import Users, db

        data = request.get_json() or {}
        gmail, password = data.get("gmail"), data.get("password")

        try:
            self.validate_inputs(gmail, password)
        except ValueError as e:
            return {"ok": True, "state": False, "error": str(e)}, 400

        if self.get_user_by_email(gmail):
            return {"ok": True, "state": False, "error": "User already exists"}, 401

        new_user = Users(gmail=gmail, password=hash_password(password))
        db.session.add(new_user)
        db.session.commit()

        return {'ok': True, 'message': 'Account successfully created', 'user_id': new_user.id}, 200

class Sign(AuthorizationBase, Resource):
    def post(self):
        """
        API for signing in to the user account
        ---
        tags:
            - Auth
        parameters:
          - name: gmail
            in: body
            type: string
            required: true
            description: User's email address
          - name: password
            in: body
            type: string
            required: true
            description: User's password
        responses:
          200:
            description: Successful sign-in
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Account successfully signed in"
                key:
                  type: object
                  properties:
                    access_token:
                      type: string
                      example: "new-access-token"
                    refresh_token:
                      type: string
                      example: "new-refresh-token"
          400:
            description: Validation error of input data
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Invalid email or password"
          404:
            description: User not found
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "User does not exist"
          401:
            description: Incorrect password
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Invalid password"
        """
        data = request.get_json() or {}
        gmail, password = data.get("gmail"), data.get("password")

        try:
            self.validate_inputs(gmail, password)
        except ValueError as e:
            return {"ok": True, "state": False, "error": str(e)}, 400

        user = self.get_user_by_email(gmail)
        if not user:
            return {"ok": True, "state": False, "error": "User does not exist"}, 401

        if not verify_password(user.password, password):
            return {"ok": True, "state": False, "error": "Invalid password"}, 401

        return {
            'ok': True, "state": True, 'message': 'Account successfully signed in',
            'key': {
                "access_token": create_access_token(identity=gmail),
                "refresh_token": create_refresh_token(identity=gmail)
            }
        }, 200

import base64
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class Update(Resource):
    @jwt_required()
    def post(self):
        """
        Create or update user profile
        ---
        tags:
          - Client
        consumes:
          - multipart/form-data
        parameters:
          - name: files
            in: formData
            type: file
            required: false
            description: List of images to upload (maximum 6)
          - name: data
            in: formData
            type: object
            required: false
            description: Profile data (e.g., name, age, etc.)
        responses:
          200:
            description: Profile successfully created or updated
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                user_id:
                  type: integer
                  example: 1
          400:
            description: Error uploading (e.g., too many images)
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
                  example: "Too many images"
        """
        # Delayed import to avoid circular import
        from app.database import Profiles, Users, Image, db

        data = request.form or {}
        files = request.files.getlist('files')
        u = Users.query.filter_by(gmail=get_jwt_identity()).first()
        image = Image.query.filter_by(profile_id=u.id).all()

        if files:
            if len(image) >= 6:
                return {'ok': False, 'state': False, 'error': 'Too many images'}, 400

            for file in files:
                photo_data = file.read()
                if photo_data:
                    db.session.add(Image(
                        profile_id=u.id,
                        photo=photo_data
                    ))

        profile = Profiles.query.filter_by(user_id=u.id).first()

        if profile:
            for key, value in data.items():
                setattr(profile, key, value)
        else:
            db.session.add(Profiles(**data, user_id=u.id))

        db.session.commit()
        return {'ok': True, 'state': False, 'user_id': u.id}, 200

class Select(Resource):
    @jwt_required()
    def get(self):
        """
        Get user profile data
        ---
        tags:
          - Client
        responses:
          200:
            description: Profile data successfully retrieved
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                name:
                  type: string
                  example: "Ivan"
                age:
                  type: integer
                  example: 25
                city:
                  type: string
                  example: "Moscow"
                sex:
                  type: string
                  example: "Male"
                search_sex:
                  type: string
                  example: "Female"
                description:
                  type: string
                  example: "I love traveling and reading books"
                image:
                  type: array
                  items:
                    type: string
                    format: base64
                    example: "/9j/4AAQSkZJRgABAQEAAAAAAAD..."
          400:
            description: Profile not found
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "No profile"
        """
        from app.database import Profiles, Users, Image

        encoded_image = []
        u = Users.query.filter_by(gmail=get_jwt_identity()).first()
        profile = Profiles.query.filter_by(user_id=u.id).first()

        if not profile:
            return {'ok': True, 'state': False, 'error': 'No profile'}, 400

        image = Image.query.filter_by(profile_id=u.id).all()
        for img in image:
            encoded_image.append(
                base64.b64encode(img.photo).decode('utf-8')
            )

        return {
            'ok': True,
            'state': False,
            'name': profile.name,
            'age': profile.age,
            'city': profile.city,
            'sex': profile.sex,
            'search_sex': profile.search_sex,
            'description': profile.description,
            'image': encoded_image,
        }

class Delete(Resource):
    @jwt_required()
    def delete(self):
        ...
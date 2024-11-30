import base64
import numpy as np
from flask import request
from sqlalchemy import or_
from flask_restful import Resource
from app.utils.coordinates import get_coordinates
from app.utils.distance import calculate_distance
from flask_jwt_extended import jwt_required, get_jwt_identity

class MatchAll(Resource):
    @jwt_required()
    def get(self):
        """
        Get a list of mutual likes (matches)
        ---
        tags:
          - Matches
        responses:
          200:
            description: Successful match list
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
                result:
                  type: object
                  additionalProperties:
                    type: object
                    properties:
                      distance:
                        type: number
                        example: 15.2
                      name:
                        type: string
                        example: "Alexey"
                      city:
                        type: string
                        example: "Moscow"
                      age:
                        type: integer
                        example: 27
                      description:
                        type: string
                        example: "I love traveling and sports"
                      img:
                        type: array
                        items:
                          type: string
                          format: base64
                          example: "/9j/4AAQSkZJRgABAQEAAAAAAAD..."
                      me_id:
                        type: integer
                        example: 1
                      peo_id:
                        type: integer
                        example: 2
                      liked_timestamp:
                        type: string
                        format: date-time
                        example: "2024-11-01T12:00:00"
                      liked_id:
                        type: integer
                        example: 123
                      liked_message:
                        type: string
                        example: "Hi, how are you?"
          404:
            description: No likes found
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "No likes found"
        """
        from app.database import Users, Likes, Profiles, Image

        me_u = Users.query.filter_by(gmail=get_jwt_identity()).first()
        me_profile = Profiles.query.filter_by(user_id=me_u.id).first()
        my_geo = get_coordinates(me_profile.city)
        result = {}

        LikesList = Likes.query.filter(
            or_(
                Likes.liker_id == me_u.id,
                Likes.liked_id == me_u.id
            ),
            Likes.liked_state == True
        ).all()

        if not LikesList:
            return {'ok': True, 'state': False, 'message': 'No likes found'}, 201

        for likes in LikesList:
            user_id = likes.liker_id if likes.liked_id == me_u.id else likes.liked_id
            peo_profile = Profiles.query.filter_by(user_id=user_id).first()
            distance, array_img = (
                calculate_distance(my_geo[0], my_geo[1], *get_coordinates(Profiles.query.filter_by(
                    user_id=(likes.liker_id if likes.liked_id == me_u.id else likes.liked_id)).first().city)),
                [base64.b64encode(img.photo).decode('utf-8') for img in Image.query.filter_by(
                    profile_id=Profiles.query.filter_by(
                        user_id=(likes.liker_id if likes.liked_id == me_u.id else likes.liked_id)).first().id).all()]
            )
            result[likes.id] = {
                'distance': distance, 'name': peo_profile.name, 'city': peo_profile.city,
                'age': peo_profile.age, 'description': peo_profile.description, 'img': array_img,
                'me_id': me_u.id, 'peo_id': likes.liker_id, 'liked_timestamp': str(likes.liked_timestamp),
                'liked_id': likes.id, 'liked_message': likes.liked_message
            }

        return {'ok': True, 'state': True, 'result': result}, 200

class LikeProfile(Resource):
    @jwt_required()
    def post(self):
        """
        Like a profile or confirm a mutual like
        ---
        tags:
          - Likes

        parameters:
          - in: formData
            name: liked_id
            type: integer
            required: false
            description: ID of the like record to confirm mutual like
          - in: formData
            name: peo_id
            type: integer
            required: false
            description: ID of the user to whom the like is given
          - in: formData
            name: liked_message
            type: string
            required: false
            description: Message with the like
        responses:
          200:
            description: Successful like or confirmation
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
          201:
            description: Like was already given earlier
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Already liked today"
        """
        from app.database import Users, Likes, check_value_in_set, add_to_set, db

        me_u = Users.query.filter_by(gmail=get_jwt_identity()).first()

        if 'liked_id' in request.form:
            likes = Likes.query.filter_by(id=request.form['liked_id']).first()
            likes.liked_id = True

            return {'ok': True, 'state': True}, 200

        message_comment = 'None' if 'liked_message' not in request.form else request.form.get('liked_message')
        if check_value_in_set(f'id:{me_u.id}', request.form['peo_id']):
            return {'ok': True, 'state': False, 'message': 'Already liked today'}, 201

        add_to_set(f'id:{me_u.id}', request.form['peo_id'])
        db.session.add(Likes(liker_id=me_u.id, liked_id=request.form['peo_id'], liked_message=message_comment))
        db.session.commit()

        return {'ok': True, 'state': True}, 200

class SkipProfile(Resource):
    @jwt_required()
    def post(self):
        """
        Remove a like (skip profile)
        ---
        tags:
          - Likes
        parameters:
          - in: formData
            name: liked_id
            type: integer
            required: true
            description: ID of the like record to delete
        responses:
          200:
            description: Successful like removal
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
          400:
            description: Record not found
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Record not found"
        """
        from app.database import Likes, db

        if 'liked_id' in request.form:
            likes = Likes.query.filter_by(id=request.form['liked_id']).first()

            if likes:
                db.session.delete(likes)
                db.session.commit()
                return {'ok': True, 'state': True}, 200
                
            return {'ok': False, 'error': 'Record not found'}, 201

        return {'ok': True, 'state': True}, 200

    

class ReadAllLikes(Resource):
    @jwt_required()
    def post(self):
        """
        Get a list of users who liked me but I haven't decided yet
        ---
        tags:
          - Matches
        responses:
          200:
            description: Successfully retrieved data
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
                distance:
                  type: number
                  example: 10.5
                name:
                  type: string
                  example: "Anastasia"
                city:
                  type: string
                  example: "Saint Petersburg"
                age:
                  type: integer
                  example: 25
                description:
                  type: string
                  example: "I love reading books and listening to music"
                img:
                  type: array
                  items:
                    type: string
                    format: base64
                    example: "/9j/4AAQSkZJRgABAQEAAAAAAAD..."
                me_id:
                  type: integer
                  example: 1
                peo_id:
                  type: integer
                  example: 3
                liked_timestamp:
                  type: string
                  format: date-time
                  example: "2024-11-01T12:00:00"
                liked_id:
                  type: integer
                  example: 456
          400:
            description: No new likes
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "No likes"
        """
        from app.database import Users, Profiles, Image, Likes

        me_u = Users.query.filter_by(gmail=get_jwt_identity()).first()
        me_profile = Profiles.query.filter_by(user_id=me_u.id).first()
        my_geo = get_coordinates(me_profile.city)

        likes = Likes.query.filter_by(
            liked_id=me_u.id,
            liked_state=False
        ).first()

        if not likes:
            return {'ok': True, 'state': False, 'message': 'No likes'}, 201

        peo_profile = Profiles.query.filter_by(user_id=likes.liker_id).first()
        distance, array_img = (
            calculate_distance(my_geo[0], my_geo[1], *get_coordinates(Profiles.query.filter_by(
                user_id=(likes.liker_id if likes.liked_id == me_u.id else likes.liked_id)).first().city)),
            [base64.b64encode(img.photo).decode('utf-8') for img in Image.query.filter_by(
                profile_id=Profiles.query.filter_by(
                    user_id=(likes.liker_id if likes.liked_id == me_u.id else likes.liked_id)).first().id).all()]
        )

        return {
            'ok': True, 'state': True, 'distance': distance, 'name': peo_profile.name, 'city': peo_profile.city,
            'age': peo_profile.age, 'description': peo_profile.description, 'img': array_img,
            'me_id': me_u.id, 'peo_id': likes.liker_id, 'liked_timestamp': str(likes.liked_timestamp),
            'liked_id': likes.id, 'liked_message': likes.liked_message
        }, 200

class SearchProfile(Resource):
    @jwt_required()
    def get(self):
        """
        Search for matching profiles
        ---
        tags:
          - Matches
        responses:
          200:
            description: Successfully retrieved profile data
            schema:
              type: object
              properties:
                ok:
                  type: boolean
                  example: true
                state:
                  type: boolean
                  example: true
                distance:
                  type: number
                  example: 12.3
                name:
                  type: string
                  example: "Ivan"
                city:
                  type: string
                  example: "Moscow"
                age:
                  type: integer
                  example: 28
                description:
                  type: string
                  example: "Traveler and artist"
                img:
                  type: array
                  items:
                    type: string
                    format: base64
                    example: "/9j/4AAQSkZJRgABAQEAAAAAAAD..."
                me_id:
                  type: integer
                  example: 1
                peo_id:
                  type: integer
                  example: 4
          400:
            description: No available profiles
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
                  example: "No matching profiles found"
        """
        from app.database import check_value_in_set, Users, Profiles, Image

        me_u = Users.query.filter_by(gmail=get_jwt_identity()).first()
        me_profile = Profiles.query.filter_by(user_id=me_u.id).first()

        if not me_profile:
            return {'ok': True, 'state': False, 'error': 'No profile found for the user'}, 201

        my_geo = get_coordinates(me_profile.city)

        peo_profiles = Profiles.query.filter(
            (Profiles.age >= (me_profile.age - 4)) &
            (Profiles.age <= (me_profile.age + 4)) &
            (Profiles.sex == me_profile.search_sex) 
        ).all()

        for peo_profile in peo_profiles:
            if not check_value_in_set(f'id:{me_u.id}', peo_profile.id):
                distance = calculate_distance(my_geo[0], my_geo[1], *get_coordinates(peo_profile.city))
                if calculate_distance(my_geo[0], my_geo[1], *get_coordinates(peo_profile.city)) <= 30:
                    array_img = [
                        base64.b64encode(img.photo).decode('utf-8')
                        for img in Image.query.filter_by(profile_id=peo_profile.id).all()
                    ]
                    break
                    
                return {
                    'ok': True, 'state': True, 'distance': distance, 'name': peo_profile.name,
                    'city': peo_profile.city, 'age': peo_profile.age, 'description': peo_profile.description,
                    'img': array_img, 'me_id': me_u.id, 'peo_id': peo_profile.id
                }, 200

        return {'ok': True, 'state': False, 'error': 'No matching profiles found'}, 201

from flask_restful import Resource
from app.utils.coordinates import get_all_city

class getAllCity(Resource):
    def get(self):
        """
        Get the list of all cities
        ---
        tags:
          - Utility

        responses:
          200:
            description: Successfully retrieved the list of cities
            schema:
              type: object
              properties:
                city:
                  type: array
                  items:
                    type: string
                  example: ["Kyiv", "Kharkiv", "Lviv", "Odessa"]
        """
        return {'city': get_all_city(country_code='UA')}

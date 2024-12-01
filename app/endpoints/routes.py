from app.models import (
    Register, Sign, RefreshToken, #Auth
    Update, Select, Delete, #Client
    SearchProfile, SkipProfile, LikeProfile, ReadAllLikes, MatchAll,# Like,
    getAllCity # Other
)
from flask import Blueprint
from flask_restful import Api

App = Blueprint('main', __name__)
api = Api(App)

# auth
api.add_resource(Sign, '/sign', methods=['POST'])
api.add_resource(Register, '/register', methods=['POST'])
api.add_resource(RefreshToken, '/refresh', methods=['POST'])

# change client
api.add_resource(Update, '/update', methods=['POST'])
api.add_resource(Select, '/select', methods=['GET'])
api.add_resource(Delete, '/delete', methods=['DELETE'])

# likes
api.add_resource(SearchProfile, '/search', methods=['GET'])
api.add_resource(SkipProfile, '/skip', methods=['POST'])
api.add_resource(LikeProfile, '/like', methods=['POST'])
api.add_resource(ReadAllLikes, '/getLike', methods=['POST'])
api.add_resource(MatchAll, '/matchAll', methods=['GET'])

# Other
api.add_resource(getAllCity, '/city', methods=['GET'])

# init
api.init_app(App)
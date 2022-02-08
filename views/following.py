from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from my_decorators import *

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here
        followings = (db.session.query(Following).join(User, User.id == Following.user_id).filter(Following.user_id == self.current_user.id).all())
        final_followings = [following.to_dict_following() for following in followings]
        return Response(json.dumps(final_followings), mimetype="application/json", status=200)

    @check_missing_user_id
    @check_valid_bookmark_following_id_format
    @check_valid_user
    @handle_db_insert_error
    def post(self):
        # Your code here
        body = request.get_json()
        user_id = body.get('user_id')
        following = Following(self.current_user.id, user_id)
        db.session.add(following)
        db.session.commit() 
        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @check_valid_user_to_unfollow_format
    @check_valid_user_to_unfollow
    @check_authorized_unfollow
    def delete(self, id):
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message' : 'Following {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

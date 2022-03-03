from flask import Response, request
from flask_restful import Resource
from models import LikePost, db
import json
from . import can_view_post
from my_decorators import *
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @check_valid_like_post_id_format
    @handle_db_insert_error
    @check_valid_patch_post_id
    @secure_like    
    def post(self, post_id):
        body = request.get_json()
        like = LikePost(self.current_user.id, post_id)
        db.session.add(like)
        db.session.commit() 
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @check_valid_delete_like_post_id_format
    @check_valid_delete_like_post_id
    @secure_delete_like
    def delete(self, post_id, id):
        # Your code here
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message' : 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps({}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

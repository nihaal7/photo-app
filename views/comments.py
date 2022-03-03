from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post
from my_decorators import *
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @check_valid_post_id_format
    @check_valid_comment_post_id
    @secure_comment
    @comment_missing_text
    def post(self):
        body = request.get_json()
        post_id = body.get('post_id')
        text = body.get('text')
        comment = Comment(text,self.current_user.id, post_id)
        db.session.add(comment)
        db.session.commit() 
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    @check_comment_id_to_delete_format
    @check_valid_comment_id
    @check_authorized_delete
    def delete(self, id):
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message' : 'Comment {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

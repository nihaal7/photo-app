from flask import Response, request
from flask_restful import Resource
from models import Bookmark, bookmark, db
import json
from . import can_view_post
from my_decorators import *

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        bookmark_list_of_dicts = [bookmark.to_dict() for bookmark in bookmarks]
        return Response(json.dumps(bookmark_list_of_dicts), mimetype="application/json", status=200)

    @check_missing_post_id
    @check_valid_bookmark_post_id_format
    @check_valid_bookmark_post_id
    @secure_bookmark
    @handle_db_insert_error
    def post(self):
        body = request.get_json()
        post_id = body.get('post_id')
        bookmark = Bookmark(self.current_user.id, post_id)
        db.session.add(bookmark)
        db.session.commit() 
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @check_valid_bookmark_id_format
    @check_valid_bookmark_id
    @check_ownership_of_bookmark
    def delete(self, id):
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message' : 'Bookmark {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

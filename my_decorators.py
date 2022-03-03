from datetime import datetime
import json
from flask import Response, request
from models.like_comment import LikeComment
from models.like_post import LikePost
from views import can_view_post
from models import Bookmark, Post, User, Following, Comment

def handle_db_insert_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            print(db_message)                   # logs it to the console
            message = 'Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json()
            # post_data['user_id'] = self.current_user.id
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

#bookmark decorators
def secure_bookmark(func):
    def wrapper(self, *args, **kwargs):
        body = request.get_json()
        post_id = body.get('post_id')
        if can_view_post(post_id, self.current_user):
            return func(self)
        else:
            response_obj = {
                'message': 'You dont have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_valid_bookmark_id_format(func):
    def wrapper(self, id):
        if isinstance(id, int):
            return func(self,id)
        elif id.isnumeric():
            return func(self,id)
        else:
            response_obj = {
                'message': 'You didnt create id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_ownership_of_bookmark(func):
    def wrapper(self, id):
        bookmark = Bookmark.query.get(id)
        if bookmark.user_id == self.current_user.id:
            return func(self, id)
        else:
            response_obj = {
                'message': 'You did not create bookmark id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)  
    return wrapper

def check_valid_bookmark_id(func):
    def wrapper(self,id):
        bk = Bookmark.query.get(id)
        if bk is not None:
            return func(self,id)
        else:
            response_obj = {
                'message': 'Bookmark ID does not exist'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_valid_bookmark_post_id_format(func):
    def wrapper(self):
        body = request.get_json()
        post_id = body.get('post_id')
        if isinstance(post_id, int):
            return func(self)
        elif post_id.isnumeric():
            return func(self)
        else:
            response_obj = {
                'message': 'You dont have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper       

def check_valid_bookmark_post_id(func):
    def wrapper(self):
        body = request.get_json()
        post_id = body.get('post_id')
        posts = Post.query.get(post_id)
        if posts is not None:
            return func(self)
        else:
            response_obj = {
                'message': 'Post ID does not exist'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_missing_post_id(func):
    def wrapper(self):
        body = request.get_json()
        post_id = body.get('post_id')
        if post_id is None:
            response_obj = {
                'message': 'You dont have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        else:
            return func(self)
    return wrapper

#following decorators
def check_valid_bookmark_following_id_format(func):
    def wrapper(self):
        body = request.get_json()
        user_id = body.get('user_id')
        if isinstance(user_id, int):
            return func(self)
        elif user_id.isnumeric():
            return func(self)
        else:
            response_obj = {
                'message': 'Incorrect ID Format for id ={0}'.format(user_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_valid_user(func):
    def wrapper(self):
        body = request.get_json()
        user_id = body.get('user_id')
        user = User.query.get(user_id)
        if user is not None and user_id != self.current_user.id:
            return func(self)
        else:
            response_obj = {
                'message': 'Incorrect user id ={0}'.format(user_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_missing_user_id(func):
    def wrapper(self):
        body = request.get_json()
        user_id = body.get('user_id')
        if user_id is None:
            response_obj = {
                'message': 'Missing user id'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        else:
            return func(self)
    return wrapper

def check_valid_user_to_unfollow(func):
    def wrapper(self,id):
        follow = Following.query.get(id)
        if follow is not None:
            return func(self,id)
        else:
            response_obj = {
                'message': 'Incorrect follow id ={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_valid_user_to_unfollow_format(func):
    def wrapper(self,id):
        if isinstance(id, int):
            return func(self,id)
        elif id.isnumeric():
            return func(self,id)
        else:
            response_obj = {
                'message': 'Invalid delete id format'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper    

def check_authorized_unfollow(func):
    def wrapper(self,id):
        follows = Following.query.get(id)
        if (follows.user_id == self.current_user.id):
            return func(self,id)
        else:
            response_obj = {
                'message': 'You are not following user: {0}'.format(id)
            }
        return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper    

#comment decorators
def check_valid_post_id_format(func):
    def wrapper(self):
        body = request.get_json()
        post_id = body.get('post_id')
        if isinstance(post_id, int):
            return func(self)
        elif post_id.isnumeric():
            return func(self)
        else:
            response_obj = {
                'message': 'Invalid format of post id = {0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_valid_comment_post_id(func):
    def wrapper(self):
        body = request.get_json()
        post_id = body.get('post_id')
        posts = Post.query.get(post_id)
        if posts is not None:
            return func(self)
        else:
            response_obj = {
                'message': 'Post ID does not exist'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def secure_comment(func):
    def wrapper(self, *args, **kwargs):
        body = request.get_json()
        post_id = body.get('post_id')
        if can_view_post(post_id, self.current_user):
            return func(self)
        else:
            response_obj = {
                'message': 'You dont have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def comment_missing_text(func):
    def wrapper(self):
        body = request.get_json()
        text = body.get('text')
        if text is not None and text!='' and len(text)!=0:
            return func(self)
        else:
            response_obj = {
                'message': 'Missing text in comment'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_comment_id_to_delete_format(func):
    def wrapper(self, id):
        if isinstance(id, int):
            return func(self,id)
        elif id.isnumeric():
            return func(self,id)
        else:
            response_obj = {
                'message': 'You didnt comment id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_valid_comment_id(func):
    def wrapper(self,id):
        comment = Comment.query.get(id)
        if comment is not None:
            return func(self,id)
        else:
            response_obj = {
                'message': 'Comment ID does not exist'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_authorized_delete(func):
    def wrapper(self,id):
        deleting = Comment.query.get(id)
        if (deleting.user_id == self.current_user.id):
            return func(self,id)
        else:
            response_obj = {
                'message': 'You didnt make comment id: {0}'.format(id)
            }
        return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper  

#post decorators
def check_valid_post_limit(func):
    def wrapper(self):
        response_obj = {
                'message': 'Bad Limit'
        }
        if 'limit' in request.args:
            limit = request.args.get('limit')
            try:
                limit = int(limit)
            except:
                return Response(json.dumps(response_obj), mimetype="application/json", status=400)
            if limit > 50:
                return func(self)
            else:
                return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return func(self)
    return wrapper

def check_post_bad_data(func):
    def wrapper(self):
        response_obj = {
                'message': 'Bad Data'
        }
        body = request.get_json()
        if body == {}:
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        else:
            return func(self)
    return wrapper

def check_valid_patch_post_id(func):
    def wrapper(self,id):
        post_id = id
        posts = Post.query.get(post_id)
        if posts is not None:
            return func(self,id)
        else:
            response_obj = {
                'message': 'Post ID does not exist'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_valid_patch_post_id_format(func):
    def wrapper(self, id):
        if isinstance(id, int):
            return func(self,id)
        elif id.isnumeric():
            return func(self,id)
        else:
            response_obj = {
                'message': 'Invalid post id format for id ={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_delete_id_format(func):
    def wrapper(self, id):
        if isinstance(id, int):
            return func(self,id)
        elif id.isnumeric():
            return func(self,id)
        else:
            response_obj = {
                'message': 'Invalid post id format for id ={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

#like post decorators
def check_valid_like_post_id_format(func):
    def wrapper(self, post_id):
        if isinstance(post_id, int):
            return func(self,post_id)
        elif post_id.isnumeric():
            return func(self,post_id)
        else:
            response_obj = {
                'message': 'Invalid post id format for id ={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def secure_like(func):
    def wrapper(self, post_id):
        if can_view_post(post_id, self.current_user):
            return func(self,post_id)
        else:
            response_obj = {
                'message': 'You dont have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper

def check_valid_delete_like_post_id_format(func):
    def wrapper(self, post_id,id):
        if isinstance(id, int):
            return func(self,post_id,id)
        elif id.isnumeric():
            return func(self,post_id,id)
        else:
            response_obj = {
                'message': 'Invalid id format for id ={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_valid_delete_like_post_id(func):
    def wrapper(self,post_id, id):
        lc = LikePost.query.get(id)
        if lc is not None:
            return func(self,post_id,id)
        else:
            response_obj = {
                'message': 'Like ID does not exist: {0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper


def secure_delete_like(func):
    def wrapper(self, post_id, id):
        lp = LikePost.query.get(id)
        if str(lp.user_id) == str(self.current_user.id):
            return func(self,post_id,id)
        else:
            response_obj = {
                'message': 'You havent liked that user_id ={0} and current user={1}'.format(lp.user_id,self.current_user.id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper
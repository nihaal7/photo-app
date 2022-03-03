from models import User
import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta

class AccessTokenEndpoint(Resource):

    def post(self):
        body = request.get_json() or {}
        # print(body)
        password = body.get('password')
        username = body.get('username')
        user = User.query.filter_by(username = username).one_or_none()
        # print(user)
        if user and user.check_password(password):
        # check username and log in credentials. If valid, return tokens
            return Response(json.dumps({ 
                "access_token": flask_jwt_extended.create_access_token(identity = user.id), 
                "refresh_token": flask_jwt_extended.create_refresh_token(identity = user.id)
            }), mimetype="application/json", status=200)
        elif user:
            return Response(json.dumps({ 
                "message" : "bad password"
            }), mimetype="application/json", status=401)
        else:
            return Response(json.dumps({ 
                "message" : "bad username"
            }), mimetype="application/json", status=401)



class RefreshTokenEndpoint(Resource):
    
    def post(self):

        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        if refresh_token:
            # https://flask-jwt-extended.readthedocs.io/en/latest/refreshing_tokens/
            # Hint: To decode the refresh token and see if it expired:
            try:
                decoded_token = flask_jwt_extended.decode_token(refresh_token)
                exp_timestamp = decoded_token.get("exp")
                user_id = decoded_token.get("sub")
                current_timestamp = datetime.timestamp(datetime.now(timezone.utc))
            except:
                 return Response(json.dumps({ 
                        "message": "error"
                    }), mimetype="application/json", status=400)
            if exp_timestamp < current_timestamp:
                return Response(json.dumps({ 
                        "message": "refresh_token has expired"
                    }), mimetype="application/json", status=401)
            else:
                return Response(json.dumps({ 
                        "access_token": flask_jwt_extended.create_access_token(identity = user_id)
                    }), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({ 
                        "message": "missing refresh token"
                    }), mimetype="application/json", status=401)

    

def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )
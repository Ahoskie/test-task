import json
import jwt

from django.http.request import HttpRequest
from django.http.response import HttpResponse

from posts.services.rest_client.rest_client import is_user_token_valid


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        api_in_request_path = request.path.lstrip('/')[:3] == 'api'
        if api_in_request_path:
            jwt_token = request.headers.get('Authorization')
            if jwt_token:
                token_type = jwt_token[:7]
                if token_type != 'Bearer ':
                    return HttpResponse(
                        content=json.dumps({'code': 'Token bad format'}),
                        content_type='application/json',
                        status=401
                    )
                jwt_token = jwt_token[7:]
                if is_user_token_valid(jwt_token):
                    user_payload = jwt.decode(jwt_token, options={'verify_signature': False})
                    jwt_user = {
                        'user_id': int(user_payload.get('user_id')),
                        'username': user_payload.get('username')
                    }
                    request.jwt_user = jwt_user
                else:
                    return HttpResponse(
                        content=json.dumps({'code': 'Token is invalid or expired'}),
                        content_type='application/json',
                        status=401
                    )
            else:
                return HttpResponse(
                    content=json.dumps({'code': 'Authentication credentials have not been provided'}),
                    content_type='application/json',
                    status=401
                )
        response = self.get_response(request)
        return response

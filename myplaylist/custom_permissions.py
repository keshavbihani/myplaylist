from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from .external_apis import Authenticate
import jwt
from rest_framework import serializers
from .user_wrapper import UserWrapper

class JWTAuthenticate(permissions.BasePermission):
    
    def get_jwt(self,request):
        ''' 
            first use "get_authorization_header" to get auth header as a tuple
            ('Bearer','<token>') 
            test:
                1. auth[0] == JWT header prefix
                    if not equal raise error
                2.  check wether the len is > 1 or not:  
                    if not raise error
                3. len shuld be less than 2 :
                    raise error

                          
        '''
        # import ipdb
        # ipdb.set_trace()
        auth = get_authorization_header(request).split()

        if not auth or auth[0].decode() != api_settings.JWT_AUTH_HEADER_PREFIX:
            msg ='Invalid Authentcation Token'
            raise AuthenticationFailed(msg)
        elif len(auth) == 1:
            msg ='Invalid Authentcation Token'
            raise AuthenticationFailed(msg)
        elif len(auth)>2:
            msg ='Some garbage data is send in auth token'
            raise AuthenticationFailed(msg)  
        return auth[1].decode()              

    def get_payload(self,jwt_token): 
        try:
            payload = jwt.decode(
                                    jwt_token,
                                    api_settings.JWT_PUBLIC_KEY,
                                    algorithms=[api_settings.JWT_ALGORITHM]
                                )
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise serializers.ValidationError(msg)

        return payload


    def has_permission(self, request, view):
        '''
            JWT token verification part
        '''

        '''
            first we need to get token from request header,
            decode token and get our payload,
            we need to check username of user in our main 
            USER model
        '''  
        if request.method not in ['GET']:  
            jwt_token = self.get_jwt(request)
            if not jwt_token:
                raise AuthenticationFailed("Invalid Authentcation Token")

            payload = self.get_payload(jwt_token)

            if not payload:
                raise AuthenticationFailed("Invalid Authentcation Token")

            username = payload['username']
            response = Authenticate.verify_user(username)
            if response.get('error'):
                raise AuthenticationFailed("Invalid Authentcation Token")
            request.user = UserWrapper.get_user_object(payload)    
        return True    

    @classmethod
    def is_permitted(cls,permission):
        def is_permitted_internal(func):    
            def Wrapped(*args,**kwargs):   
                request = args[1]
                if permission not in request.user.roles:
                    raise PermissionDenied
                return func(*args,*kwargs)
            return Wrapped

        
        return is_permitted_internal    
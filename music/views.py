from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from .serializers import SongSerializer,PlaylistSerializer,PlaylistSerializerCreate,PlaylistSerializerUpdate
from .models import Songs,Playlist,UserPlaylistMapping
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from myplaylist.custom_permissions import JWTAuthenticate
# @api_view()
# def hello_world(request):
#     return Response({"message": "Hello, world!"})

from rest_framework import permissions
from myplaylist.external_apis import S3

@api_view(['POST'])
def post_song(request):
    '''
        storing song objects in aws s3 and storing key of 
        those song objects in Song table
    '''
    fileObj = request.data.get('fileObj')
    artist = request.data.get('artist')
    music_type = request.data.get('music_type')
    name = request.data.get('name')

    S3.upload(fileObj,f'media/public/{fileObj.name}')
    song_obj = Songs.objects.create(name = name,
                        artist=artist,
                        music_type = music_type,
                        song_key = f'media/public/{fileObj.name}')
    if song_obj:
        return Response({'data':'uploaded'},status=status.HTTP_200_OK)
    return Response({'data':'error'},status=status.HTTP_400_BAD_REQUEST)    

@api_view()
#@permission_classes([IsAdminUser])
def get_all_songs(request):
    '''
        we will get all songs objects from our databse, then we need to convert
        objects into dictionaries /python datatype, we need to send the response

    '''
    s = Songs.objects.all()
    response = SongSerializer(s,many=True).data
    return Response(response)



class PlaylistViews(APIView):
    # permission_classes = [JWTAuthenticate]
    #authentication_classes = [SessionAuthentication]
    # @JWTAuthenticate.is_permitted('AllowReadPlaylist')    
    def get(self,request): #args =[self,request]
        p = Playlist.objects.all()
        response = PlaylistSerializer(p,many=True).data
        return Response(response)

    @JWTAuthenticate.is_permitted('AllowCreatePlaylist')        
    def post(self,request):
        '''
            request.data
            {
                "name":"hi",
                "songs":[11,12],
            }
            first validate the request data, then save the data in 
            Playlist model
            {
                "name":"hi",
                "songs":[11,12],
                "user":<id of request.user object>
            }


        '''
        print(request.user)
        user_obj = UserPlaylistMapping.objects.filter(user_id = request.user.user_id).last()
        request.data['user']=user_obj.id
        serializer = PlaylistSerializerCreate(data = request.data)  
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"invalid data"},status=status.HTTP_400_BAD_REQUEST)  



class PlaylistDetailViews(APIView):
    permission_classes = [JWTAuthenticate]

    def get(self,request,id):
        p = Playlist.objects.filter(id=id).last()
        if p:
            response = PlaylistSerializer(p).data
            return Response(response)
        return Response({"message":"invalid id"},status=status.HTTP_400_BAD_REQUEST)        

    @JWTAuthenticate.is_permitted('AllowUpdatePlaylist')
    def patch(self,request,id):
        '''
            request.data
            {
                "name":"hithere",
                "songs":[13],
                "event":"add_song/remove_song"
            }
            
            we will take this request.data and we are going to update
            playlist object with given data using update function in
            our serializer class
        ''' 
        user_obj = UserPlaylistMapping.objects.filter(user_id = request.user.user_id).last()
        request.data['user']=user_obj.id
        #request.data['name'] = request.data.get('name',p.name)
        p = Playlist.objects.filter(id=id).last()
        self.check_object_permissions(request, p)
        request.data['name'] = request.data.get('name',p.name)
        serializer = PlaylistSerializerUpdate(p,data = request.data,context = {"event":request.data.get('event')})  
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"invalid data"},status=status.HTTP_400_BAD_REQUEST)  


@api_view()
def cpu_intensive(request):
    try:
        factorial = 1
        for i in range(1,100000):
           factorial = factorial*i
        return Response({"message":"done"},status=status.HTTP_200_OK)   
    except Exception as e:
        return Response({"message":e},status=status.HTTP_400_BAD_REQUEST)       
       
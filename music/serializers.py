from rest_framework import serializers
from .models import Songs,Playlist
from myplaylist.external_apis import S3

class SongSerializer(serializers.ModelSerializer):
    song_url = serializers.SerializerMethodField()
    class Meta:
        model = Songs
        fields = '__all__'

    def get_song_url(self,obj):
        return S3.get_signed_url(obj.song_key) if obj.song_key  else obj.song_key   

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    #user = UserSerializer()

    class Meta:
        model = Playlist
        fields = '__all__'    



class PlaylistSerializerCreate(serializers.ModelSerializer):
   
    class Meta:
        model = Playlist
        fields = '__all__'           


    def validate_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("numeric value not allowed in playlist name")
        return value

    def validate(self,data):
        print(data)
        return data    

class PlaylistSerializerUpdate(serializers.ModelSerializer):
    

    class Meta:
        model = Playlist
        fields = '__all__'           


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        #instance.songs = validated_data.get('songs', instance.songs)
        #print(validated_data)
        if self.context.get('event')=='add_song':
            instance.songs.add(*(validated_data.get('songs', instance.songs)))
            

        elif self.context.get('event')=='remove_song':
            instance.songs.remove(*(validated_data.get('songs', instance.songs)))
        instance.save()
        return instance    
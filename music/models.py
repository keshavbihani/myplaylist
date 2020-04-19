from django.db import models
from django.conf import settings
# Create your models here

class UserPlaylistMapping(models.Model):
	user_id = models.IntegerField(unique=True)
	username = models.CharField(max_length=255)

	def __str__(self):
		return self.username

class Songs(models.Model):
	name = models.CharField(max_length=100)
	artist = models.CharField(max_length=100,blank=True,null=True)
	music_type = models.CharField(max_length=30,blank=True,null=True)
	song_key = models.CharField(max_length=255,blank=True,null=True)

	def __str__(self):
		return self.name

class Playlist(models.Model):
	name = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	songs = models.ManyToManyField(Songs)
	user = models.ForeignKey(UserPlaylistMapping,on_delete=models.CASCADE)

	def __str__(self):
		return self.name
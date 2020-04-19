from myplaylist.celery_app import app
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from .models import Playlist,UserPlaylistMapping

@app.task
def top_three_playlist():
	
	try:
		playlists = Playlist.objects.all()[:3]

		mail_body= 'Top three Weekly:   '
		for playlist in playlists:
			mail_body += f'http://localhost:8080/music/playlist/{playlist.id}   '

		
		users = UserPlaylistMapping.objects.all()
		for user in users:	
			send_mail(
			    "Weekly Top 3!",
			    mail_body,
			    settings.EMAIL_HOST_USER,
			    ['bihanikeshav123@gmail.com']
				)	
	except SMTPException as e:
		print(e)		
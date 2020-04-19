import requests
import boto3
from botocore.client import Config

class Authenticate():

    @classmethod
    def verify_user(cls,username=None):
        if username:
            response = requests.get('http://localhost:8000/accounts/verify_user_by_username?username='+username)
            return response.json()
        return dict({'error':'invalid data'})   


class S3():

    @classmethod
    def get_client(cls):
        client =  boto3.client( 
        's3', 
        aws_access_key_id='AKIA323XERZKNKEBP7FJ', 
        aws_secret_access_key='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',
        region_name = 'ap-south-1',
        config = Config(s3={'addressing_style':'path'}) 
        )
        return client  

    @classmethod
    def upload(cls,fileObj,key,bucket = 'myplaylist-assests'):
        client = S3.get_client()
        client.upload_fileobj(fileObj,bucket,key)

    
    @classmethod    
    def get_signed_url(cls,key,expiration=3600,bucket_name='myplaylist-assests'):
        client = S3.get_client()
        return client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': key,
                                                            'ResponseContentType':'audio/mp3'},
                                                    ExpiresIn=expiration)    
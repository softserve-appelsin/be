import boto3
from django.conf import settings
from .models import Track
import io

def get_track_file_from_aws(track: Track):
    
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f'media/{track.file.name}')
    file_bytes = response['Body'].read()
    file_object = io.BytesIO(file_bytes)
    
    return file_object

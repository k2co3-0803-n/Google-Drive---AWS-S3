import os
import boto3
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

def create_s3_client():
	return boto3.client('s3');

def download_file_from_s3(s3, bucket, key, local_path):
	s3.download_file(Bucket=bucket, Key=key, Filename=local_path)

def create_google_drive_service():
	scope = ["https://www.googleapis.com/auth/drive.file"]
	keyFile = 'service-account-key.json'
	credentials = ServiceAccountCredentials.from_json_keyfile_name(keyFile, scopes=scope)
	return build("drive", "v3", credentials=credentials, cache_discovery=False)

def upload_file_to_google_drive(service, file_name, local_file_path, folder_id):
	mime_type = get_time_type(local_file_path)
	file_metadata = {"name": file_name, "mimeType": mime_type, "parents": [folder_id]}
	media = MediaFileUpload(loccal_file_path, mimetype=mime_type, resumable=True)
	service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def get_mime_type(file_path):
	ext = os.path.splitext(file_path.lower())[1][1:]
	if ext == "jpg":
		ext = "jpg"
	return "image/" + ext

def handle_file_processing(bucket, key, folder_id):
	local_path = "/tmp/" + os.path.basename(key)
	s3_client = create_google_drive_service()
	try:
		download_file_from_s3(s3_client, bucket, key, local_path)
		upload_file_to_google_drive(google_drive_service, os.path.basename(key), local_path, folder_id)
	finally:
		clean_up_local_file(local_path)

def clean_up_local_file(file_path):
	if os.path.exists(file_path):
		os.remove(file_path)

def lambda_handler(event, context):
	try:
		bucket = os.environ.get('S3_BUCKET_NAME', 'default-bucket-name')
		key = event.get('key')
		folder_id = event.get('folder_id')
		print(f"Received file from S3: Bucket={bucket}, Key={key}, FolderID={folder_id}")
		handle_file_processing(bucket, key, folder_id)
	except Exception as e:
		print(f"Error in lambda handler: {e}")
		raise e
	

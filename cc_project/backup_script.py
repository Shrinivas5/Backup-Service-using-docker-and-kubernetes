from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Define scope
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    # Load credentials from credentials.json file
    if os.path.exists('credentials.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        print("Error: 'credentials.json' file not found.")
    return creds

def upload_file_to_drive(file_path, drive_folder_id):
    # Authenticate and create a Drive service
    creds = authenticate()
    if creds:
        service = build('drive', 'v3', credentials=creds)

        # Set the file metadata
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [drive_folder_id]  # ID of the folder where you want to upload the file
        }

        # Upload the file
        media = MediaFileUpload(file_path, resumable=True)
        try:
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print('File uploaded successfully. File ID: %s' % file.get('id'))
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    file_path = 'C:\\Users\\icc\\Desktop\\cc_project\\test_file.txt'  # Change this to the path of your file
    drive_folder_id = '1IIdUUYn6_ylfUjvNTdbr1uRY65nT5TwK'
    upload_file_to_drive(file_path, drive_folder_id)

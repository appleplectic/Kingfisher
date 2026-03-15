from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
import io

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
PATH = "sar-dataset/images/val/"
FOLDER_ID = "1d94HfOZnhyOUKJ9LvdK9Oh-7DOmWP3Ru"
ARGS = {
    "q": f"'{FOLDER_ID}' in parents and name contains '.jpg'",
    "pageSize": 600,
    "spaces": "drive",
    "fields": "nextPageToken, files(id, name)"
}

# Obtain your Google credentials
def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    return flow.run_local_server(port=0)

def main():
    # Build the downloader
    creds = get_credentials()
    drive_downloader = build('drive', 'v3', credentials=creds)
    file_request = drive_downloader.files().list(**ARGS).execute()
    files = file_request.get('files', [])
    next_page_token = file_request.get('nextPageToken', None)
    while next_page_token:
        file_request = drive_downloader.files().list(
            **ARGS, pageToken=next_page_token
        ).execute()
        files.extend(file_request.get('files', []))
        next_page_token = file_request.get('nextPageToken', None)

    for file_num in range(0, len(files)):
        file = files[file_num]
        dotjpg_str_idx = file['name'].index('.jpg')
        if int(file['name'][3: dotjpg_str_idx]) >= 1310:
            continue
        print("file being downloaded: " + file['name'])
        request = drive_downloader.files().get_media(fileId=file['id'])
        file_io = io.FileIO(PATH + file['name'], 'wb')
        downloader = MediaIoBaseDownload(file_io, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
    print("Download finished...hopefully it worked.")

if __name__ == '__main__':
    main()

import os.path, csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# scopes for Calendar & Tasks
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

def main():
    return

def create_needed_directories():
    """_summary_
    """
    if not os.path.isdir('token'):
        os.makedirs('token')
    if not os.path.isdir('imports'):
        os.makedirs('imports')
    if not os.path.isdir('credentials'):
        os.makedirs('credentials')
    return

def get_services():
    """_summary_

    Returns:
        _type_: _description_
    """
    creds = None
    if os.path.exists('token/token.json'):
        creds = Credentials.from_authorized_user_file('token/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token/token.json', 'w') as token:
            token.write(creds.to_json())

    calendar_service = build('calendar', 'v3', credentials=creds)
    tasks_service = build('tasks', 'v1', credentials=creds)
    return calendar_service, tasks_service


if __name__ == '__main__':
    main()
    
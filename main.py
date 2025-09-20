import os.path
import csv
import tzlocal
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from zoneinfo import ZoneInfo

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

def read_csv():
    for import_file in os.listdir('/imports'):
        if import_file.lower().endswith(".csv"):
            full_path = os.path.join('/imports', import_file)
            with open(full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row["title"]
                    location = row["location"]
                    description = row["description"]
                    start = row["start"]
                    end = row["end"]
                    action = row["action"]

                    if action == "event":
                        print("test")
                    else:
                        print("test")


                    print(f"Title: {title}, Location: {location}, Description: {description}, Start: {start}, End: {end}")
        else:
            print("there is no csv in the imports folder, please put one")
    return

def create_calendar_event(service):
    local_zone = ZoneInfo(tzlocal.get_localzone_name())

    event = {
        'summary': 'Demo Meeting',
        'location': 'Online',
        'description': 'Discuss project goals.',
        'start': {'dateTime': '2025-09-10T15:00:00-06:00', 'timeZone': str(local_zone)},
        'end':   {'dateTime': '2025-09-10T16:00:00-06:00', 'timeZone': str(local_zone)}
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print("Created event:", created_event.get('htmlLink'))

def create_task(service):
    task = {
        'title': 'Finish STAT 151 Homework',
        'notes': 'Complete Module 3 questions',
        'due': '2025-09-15T23:59:00.000Z'   # UTC in RFC3339 format
    }
    created_task = service.tasks().insert(tasklist='@default', body=task).execute()
    print("Created task:", created_task['title'])

if __name__ == '__main__':
    main()
    
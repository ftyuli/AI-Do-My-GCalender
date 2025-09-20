import os.path
import csv
import tzlocal
import shutil
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
    """this is the entry point of the program dumbass lmao

    calls create_directories() and read_csv(), pretty self explanitory
    functions
    """
    create_directories()
    read_csv()
    return

def create_directories():
    """ensures the required local folders exist

    if they dont exist it creates token/, imports/ and credentials/
    exhausted/ directories in the current working directory
    """
    if not os.path.isdir('token'):
        os.makedirs('token')
    if not os.path.isdir('imports'):
        os.makedirs('imports')
    if not os.path.isdir('credentials'):
        os.makedirs('credentials')
    if not os.path.isdir('exhausted'):
        os.makedirs('exhausted')
    return

def get_services():
    """authenticate and return google api service shit I think

    This Performs the necessary Oauth2 authentication for both google 
    calendar and google tasks. it uses token/token.json if it exist but 
    else if it opens main user browser for them to login using the credentials
    of credentials/credentials.json

    Returns:
        tuple: (calendar_service, tasks_service) where each is a
        googleapiclient.discovery.Resource object for its api
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
    """process and read all the csv files in the imports/ direcotry 

    for each csv row it split the columns into
    title, location, description, start, end, action:

        * If action == "event": create a google calendar event.
        * If action == "task":  create a google task.

    Expects start/end times in "%Y-%m-%d %H:%M" format (local time).
    """
    calendar_service, tasks_service = get_services()
    local_zone = ZoneInfo(tzlocal.get_localzone_name())

    csv_files = [f for f in os.listdir('imports') if f.lower().endswith('.csv')]
    if not csv_files:
        print("No CSV file in 'imports' folder.")
        return

    for import_file in csv_files:
        full_path = os.path.join('imports', import_file)
        with open(full_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            #next(reader)
            
            for row in reader:
                title = row["title"]
                location = row["location"]
                description = row["description"]
                start = row["start"]
                end = row["end"]
                action = row["action"].strip().lower()

                if action == "event":
                    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M").replace(tzinfo=local_zone)
                    end_dt   = datetime.strptime(end,   "%Y-%m-%d %H:%M").replace(tzinfo=local_zone)
                    create_calendar_event(calendar_service, title, location,
                                          description, start_dt.isoformat(),
                                          end_dt.isoformat())
                elif action == "task":
                    if end:
                        due_dt_local = datetime.strptime(end, "%Y-%m-%d %H:%M").replace(tzinfo=local_zone)
                    elif start:
                        due_dt_local = datetime.strptime(start, "%Y-%m-%d %H:%M").replace(tzinfo=local_zone)
                    else:
                        continue
                    due_dt_utc = due_dt_local.astimezone(ZoneInfo("UTC"))
                    create_task(tasks_service, title, description, due_dt_utc.isoformat())
                else:
                    print(f"Unknown action type: {action}")
        shutil.move(full_path, os.path.join('exhausted', import_file))
        print(f"Moved {import_file} to exhausted/")
    return

def create_calendar_event(service, summary, location, description, start, end):
    """create da gcalender event

    Args:
        service (googleapiclient.discovery.Resource): Calendar API client.
        summary (str): Event title.
        location (str): Event location (may be empty).
        description (str): Event description.
        start (str): Start time in RFC3339/ISO format with timezone.
        end (str): End time in RFC3339/ISO format with timezone.
    
    also prints the shit
    """
    local_zone = ZoneInfo(tzlocal.get_localzone_name())

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime': start, 'timeZone': str(local_zone)},
        'end':   {'dateTime': end, 'timeZone': str(local_zone)}
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created event {summary} at {created_event.get('htmlLink')}")
    return

def create_task(service, title, notes, due):
    """create google task

    Args:
        service (googleapiclient.discovery.Resource): Tasks API client.
        title (str): Task title.
        notes (str): Optional task notes/description.
        due (str): Due date-time in UTC RFC3339 format.

    also prints its shit too
    """
    task = {
        'title': title,
        'notes': notes,
        'due': due
    }
    created_task = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"Created task: {created_task['title']}, due {due}")
    return

if __name__ == '__main__':
    main()
    
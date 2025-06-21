import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def add_event(summary, description, start_dt, end_dt):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': str(start_dt.tzinfo)},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': str(end_dt.tzinfo)},
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event

def delete_event_by_summary(title):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        if event.get('summary', '').lower() == title.lower():
            service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
            return True
    return False

def get_todays_events():
    service = get_calendar_service()
    tz = pytz.timezone("America/Toronto")
    now = datetime.now(tz)
    start_of_day = tz.localize(datetime(now.year, now.month, now.day, 0, 0, 0))
    end_of_day = start_of_day + timedelta(days=1)

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

import base64
from datetime import datetime, timezone
import re
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
#  python3 -m pip install python-dateutil <-- required dependency
from dateutil.relativedelta import relativedelta
import urllib

SERVICE_ACCOUNT_FILE = 'csxl-academic-advising-feature.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Global academic advising calendar ID
calendar_id_global = 'fc6f3c360534b8dc34022e7d0224c8db328033f147cd79d8454388bf15800ec0@group.calendar.google.com'

# grabbing the events from today -> 6 months from now every time the webhook notifies or our reocurring script 
# drop table first
def upcoming_events(calendar_id, creds):  # type: ignore
    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(timezone.utc).isoformat()
    six_months_later = (datetime.now(timezone.utc) + relativedelta(months=6)).isoformat()

    # Call the Calendar API
    print("Getting the upcoming events from today to six months later")
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=six_months_later,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return {}

    # Dictionary to store event details
    events_dict = {}

    for event in events:
        event_id = event["id"]

        original_summary = event.get('summary', '')
        link = event.get('htmlLink')

        # Clean and normalize the event title
        original_summary = re.sub(r'[-–—]+', ' ', original_summary)  # Replace multiple dashes with a space
        cleaned_summary = re.sub(r'[^\w\s-]', '', original_summary).strip()  # Remove special characters
        cleaned_summary = re.sub(r'\s+', ' ', cleaned_summary)  # Remove extra spaces

        # Parse start and end times
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        # Convert to datetime objects for better handling
        start_datetime = datetime.fromisoformat(start)
        end_datetime = datetime.fromisoformat(end)

        # Extract date and time components
        start_date = start_datetime.date()  # YYYY-MM-DD
        start_time = start_datetime.time()  # HH:MM:SS
        end_time = end_datetime.time()  # HH:MM:SS

        # Populate the dictionary
        events_dict[event_id] = {
            "summary": cleaned_summary,
            "start": start_time,
            "end": end_time,
            "date": start_date,
            "link": link,
        }

        # Optional: Debugging output
        print(
            f'ID: {event_id}, Summary: {cleaned_summary}, Start Date: {start_date}, '
            f'Start Time: {start_time}, End Time: {end_time}, Link: {link}'
        )

    return events_dict


if __name__ == '__main__':
   creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
   upcoming_events(calendar_id_global, creds)
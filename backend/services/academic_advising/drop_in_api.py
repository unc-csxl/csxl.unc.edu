import base64
from datetime import datetime, timezone
import re
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
#  python3 -m pip install python-dateutil <-- required dependency
from dateutil.relativedelta import relativedelta
import urllib

# grabbing the events from today -> 6 months from now every time the webhook notifies of our reocurring script 
# drop table first

# credentials to call API, will eventually be stored in db
SERVICE_ACCOUNT_FILE = 'csxl-academic-advising-feature.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# Global academic advising calendar ID
calendar_id_global = 'cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com'


def get_events(calendar_id, creds): # type: ignore
    """Calls events().list to retrieve all events within a 6 month range from today to populate database 
    
        Args: 
            calendar_id: the id of the calendar, to be stored as a credential 
            creds: required credentials to make the API call

        Returns: 
            events_result: API response
    """
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
            maxResults=2,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    
    # print(f'{events_result}')
    return events_result

def upcoming_events(events_result):  # type: ignore
    """ Parses events_result API response into a dictionary for processing and inserting into database 
    
        Args: 
            event_result: Returned response from get_events()

        Returns: 
            events_dict: dictionary with each event 
    """
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

    print(f'{events_dict}')
    return events_dict


if __name__ == '__main__':
    upcoming_events(get_events(calendar_id_global, creds))
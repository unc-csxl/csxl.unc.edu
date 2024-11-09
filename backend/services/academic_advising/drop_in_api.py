import base64
from datetime import datetime, timezone
import re
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import urllib

SERVICE_ACCOUNT_FILE = 'csxl-academic-advising-feature.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Global academic advising calendar ID
calendar_id_global = 'cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com'

def generate_event_urls(event_id, calendar_id): # type: ignore
    # Split the event ID to get only the part before the '@'
    split_event_id = event_id.split('@')[0]
    
    # Concatenate the event ID with the calendar ID
    encoded_id = f"{split_event_id} {calendar_id}"
    
    # Encode in base64 and strip any '==' padding
    base64_encoded_id = base64.b64encode(encoded_id.encode()).decode().replace("==", "")
    
    # Construct the "View Event" URLs
    view_url = f"https://www.google.com/calendar/event?eid={base64_encoded_id}"

    print("View URL:", view_url)      


def upcoming_events(calendar_id, creds): # type: ignore
    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(timezone.utc).isoformat()
    print(now)
    exit

    # Call the Calendar API
    # now = datetime.datetime.now()  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      event_id = event["id"]

      original_summary = event.get('summary', '')

      # Parsing event title (summary) for consistency in the database and for display

      # Step 1: Replace multiple hyphens, em dashes, or en dashes with a single space
      original_summary = re.sub(r'[-–—]+', ' ', original_summary)

      # Step 2: Remove any remaining special characters except single spaces and single hyphens
      cleaned_summary = re.sub(r'[^\w\s-]', '', original_summary).strip()

      # Step 3: Remove extra spaces that may result from Step 1
      cleaned_summary = re.sub(r'\s+', ' ', cleaned_summary)
      
      start = event["start"].get("dateTime", event["start"].get("date"))
      end = event["end"].get("dateTime", event["end"].get("date"))

      start_datetime = datetime.fromisoformat(start)
      start_date = start_datetime.date()  # YYYY-MM-DD
      start_time = start_datetime.time()  # HH:MM:SS
      end_datetime = datetime.fromisoformat(end)
      end_time = end_datetime.time()  # HH:MM:SS

      generate_event_urls(event_id, calendar_id_global)
      print(f'  {cleaned_summary}, Start time: {start_time}, End time: {end_time}, {event_id}, {start_date}')


if __name__ == '__main__':
   
   creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

   upcoming_events(calendar_id_global, creds)
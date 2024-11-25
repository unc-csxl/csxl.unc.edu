from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
import uuid

SERVICE_ACCOUNT_FILE = "csxl-academic-advising-feature.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events.readonly",
    "https://www.googleapis.com/auth/calendar",
]


def subscribe_to_calendar_changes(calendar_id, webhook_url): # type: ignore
    # Authenticate using service account
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    calendar_service = build("calendar", "v3", credentials=creds)

    # Create a unique ID for your webhook channel
    channel_id = str(uuid.uuid4())

    # Set up the webhook channel request
    request_body = {
        "id": channel_id,
        "type": "web_hook",
        "address": webhook_url,
        "params": {
            "ttl": "2592000"  # Channel expiration (optional, 30 days in seconds), you need to look into auto-renewing subscription
        },
    }

    # Subscribe to changes for the specified calendar
    response = (
        calendar_service.events()
        .watch(calendarId=calendar_id, body=request_body)
        .execute()
    )
    print("Webhook subscription created:", response)


if __name__ == "__main__":
    calendar_id = "cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com"
    webhook_url = "https://two-webs-start.loca.lt/notifications"  # The URL where you want to receive the notifications
    subscribe_to_calendar_changes(calendar_id, webhook_url)
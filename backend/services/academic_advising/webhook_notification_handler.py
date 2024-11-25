from flask import Flask, jsonify, request
from google.oauth2.service_account import Credentials
from backend.services.academic_advising.drop_in_api import upcoming_events
from backend.services.academic_advising.drop_in import DropInService
from typing import Self

app = Flask(__name__)


# command to start app python -m backend.services.academic_advising.webhook_notification_handler

# Set your Google credentials file and calendar ID
SERVICE_ACCOUNT_FILE = "csxl-academic-advising-feature.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# creds
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# calendar id for watched resource
calendar_id_global = "cs.unc.edu_340oonr4ec26n1fo9l854r3ip8@group.calendar.google.com"


@app.route("/notifications", methods=["POST"])
def notifications():
    # Print the incoming request body for debugging
    print("Request Body:", request.get_data())

    resource_state = request.headers.get("X-Goog-Resource-State")
    resource_id = request.headers.get("X-Goog-Resource-ID")
    print(f"Resource State: {resource_state}, Resource ID: {resource_id}")

    events = upcoming_events(calendar_id_global, creds)
    drop_in_service = DropInService()
    drop_in_service.insert_all_events(events)
    print(f"{drop_in_service.all()}")
    return "", 200  # Return 200 OK to acknowledge receipt


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

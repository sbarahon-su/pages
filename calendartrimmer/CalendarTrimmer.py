import requests
from ics import Calendar, Event
from datetime import datetime, timedelta, timezone

# Blackboard ICS Feed URL
ICS_URL = "https://blackboard.syracuse.edu/webapps/calendar/calendarFeed/c16a35588ed3475895aa4ebc5a1a18f4/learn.ics"

# Keywords to filter out (e.g., office hours, meetings)
EXCLUDE_KEYWORDS = ["Office Hours", "Meeting", "Lecture, Recitation"]

# Define the time range: 1 week before today up to the future
now = datetime.now(timezone.utc)
one_week_ago = now - timedelta(days=7)

def fetch_and_filter_ics(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch ICS file.")
        return None
    
    # Load the ICS calendar
    calendar = Calendar(response.text)

    # Filter events: keep only those within the past week or in the future
    filtered_events = [
        event for event in calendar.events
        if event.begin >= one_week_ago and not any(keyword.lower() in event.name.lower() for keyword in EXCLUDE_KEYWORDS)
    ]

    if not filtered_events:
        print("No recent or future assignments found after filtering.")

    # Create new filtered calendar
    filtered_calendar = Calendar(events=filtered_events)

    # Overwrite the ICS file (clearing old data)
    with open("filtered_calendar.ics", "w") as f:
        f.writelines(filtered_calendar)

    print(f"Filtered ICS file updated: {len(filtered_events)} events kept.")

# Run the function
fetch_and_filter_ics(ICS_URL)

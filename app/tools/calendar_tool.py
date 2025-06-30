
from langchain_core.tools import tool
from typing import List, Dict
import datetime

@tool
def calendar_scheduler_tool(story_allocations: List[Dict], sprint_days: int = 5, sprint_count: int = 2, start_date: str = None) -> List[Dict]:
    """
    Distribute assigned stories across sprints and generate a timeline with dates.
    """
    if not start_date:
        start = datetime.date.today()
    else:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

    sprint_plan = []
    current_day = start
    story_index = 0

    for sprint_num in range(1, sprint_count + 1):
        for _ in range(sprint_days):
            if story_index >= len(story_allocations):
                break

            story = story_allocations[story_index]
            sprint_plan.append({
                "sprint": f"Sprint {sprint_num}",
                "date": current_day.isoformat(),
                "assigned_to": story.get("assigned_to"),
                "email": story.get("email", "unknown"),
                "title": story.get("title"),
                "developer_type": story.get("developer_type", ""),
                "match_score": story.get("match_score", 0)
            })
            current_day += datetime.timedelta(days=1)
            story_index += 1

        current_day += datetime.timedelta(days=2)  # buffer between sprints

    return sprint_plan




'''from phi.tools.googlecalendar import GoogleCalendarTools
from langchain_core.tools import tool
import os

calendar = GoogleCalendarTools(credentials_path="credentials.json")

@tool
def create_google_event(summary: str, date: str, email: str, description: str = "") -> str:
    """
    Create a calendar event on the given date and notify the attendee.
    """
    calendar.create_event({
        "summary": summary,
        "start": {"date": date, "timeZone": "UTC"},
        "end": {"date": date, "timeZone": "UTC"},
        "attendees": [{"email": email}],
        "description": description
    })
    return f"Event created for {email} on {date}: {summary}"





    # File: app/tools/google_calendar_tool.py

from langchain_core.tools import tool
from phi.tools.googlecalendar import GoogleCalendarTools

# Initialize calendar tool once with OAuth credentials
calendar_tool = GoogleCalendarTools(credentials_path="credentials.json")

@tool
def create_google_event(summary: str, date: str, email: str, description: str = "") -> str:
    """
    Create a calendar event and send invite using Google Calendar.
    """
    event = {
        "summary": summary,
        "start": {"date": date, "timeZone": "UTC"},
        "end": {"date": date, "timeZone": "UTC"},
        "attendees": [{"email": email}],
        "description": description
    }

    calendar_tool.create_event(event)
    return f"✅ Event created for {email} on {date}: {summary}"

'''
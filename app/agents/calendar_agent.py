# File: app/agents/calendar_scheduler_agent.py

from app.agentstate.agent_state import AgentState
from app.tools.calendar_tool import calendar_scheduler_tool

def calendar_scheduler_agent(state: AgentState) -> AgentState:
    try:
        allocations = state.story_allocations

        # Run the calendar scheduler tool to generate sprint plan
        timeline = calendar_scheduler_tool.invoke({
            "story_allocations": allocations,
            "sprint_days": 5,
            "sprint_count": 2,
            "start_date": None  # or "YYYY-MM-DD" if manually set
        })

        # Update agent state
        state["sprint_schedule"] = timeline
        state["current_agent"] = "timeline_agents"
        print("📅 Sprint timeline created successfully")

    except Exception as e:
        state.error_message = str(e)
        state.current_agent = "error"
        print("❌ Failed in calendar scheduler agent:", e)

    return state










'''from app.tools.google_calendar_tool import create_google_event

def google_calendar_agent(state: AgentState) -> AgentState:
    try:
        for task in state.sprint_schedule:
            create_google_event.invoke({
                "summary": task["title"],
                "date": task["date"],
                "email": task["email"],
                "description": f"{task['developer_type']} task for {task['sprint']}"
            })

        state.current_agent = "reporting_agent"
    except Exception as e:
        state.error_message = str(e)
        state.current_agent = "error"
    return state
'''
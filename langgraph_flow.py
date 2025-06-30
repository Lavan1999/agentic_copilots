from langgraph.graph import StateGraph, END
from app.agentstate.agent_state import AgentState
from app.agents.idea_agent import idea_agent 
from app.agents.story_agent import story_agent
from app.agents.allocator_agent import story_allocator
from app.agents.calendar_agent import calendar_scheduler_agent


def build_app():
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("idea_analysis", idea_agent)
    workflow.add_node("story_planner", story_agent)
    workflow.add_node("story_allocator", story_allocator)
    workflow.add_node("calendar_agent", calendar_scheduler_agent)

    # Edges
    workflow.set_entry_point("idea_analysis")
    workflow.add_edge("idea_analysis", "story_planner")
    workflow.add_edge("story_planner", "story_allocator")
    workflow.add_edge("story_allocator", "calendar_agent")
    workflow.add_edge("calendar_agent",END)

    return workflow.compile()

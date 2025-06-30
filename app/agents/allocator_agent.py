# File: app/agents/allocator_agent.py

from app.tools.story_allocator_tool import story_allocator_tool
from app.agentstate.agent_state import AgentState

def story_allocator(state: AgentState) -> AgentState:
    try:
        story_json = state.story_json
        team_metadata = state.team_metadata
        product_title = state.product_title or "default_project"

        # 🔁 Call LLM-based allocator tool
        response = story_allocator_tool.invoke({
            "story_json": story_json,
            "team_metadata": team_metadata,
            "product_title": product_title
        })

        # Save result into state
        state["story_allocations"] = response
        state["current_agent"] = "calendar_agent"
        print("📌 Allocator Result:", response)

    except Exception as e:
        state.error_message = str(e)
        state.current_agent = "error"

    return state
'''
def story_agent(state: AgentState) -> AgentState:
    try:
        # 1. Get idea analysis output from previous agent
        story_idea = state.get("idea_analysis_result", "")

        # 2. Invoke the story_tool (LLM) to get the markdown task breakdown
        response = story_tool.invoke({
            "idea_analysis_result": story_idea,
        })

        # 3. Save the markdown table into state
        state["story_markdown"] = response

        # 4. Convert markdown to Excel and upload to MongoDB
        excel_status = convert_story_to_excel.invoke({
            "story_markdown": response,
            "product_title": state.get("product_title", "untitled_project")
        })
        state["story_excel_status"] = excel_status

        # 5. Move to next agent
        state["current_agent"] = "next_agent"
        print("✍️ story_agent markdown:", response)

    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"

    return state

'''
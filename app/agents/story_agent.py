from app.agentstate.agent_state import AgentState
from app.tools.story_tool import story_tool
from app.tools.csv_excel_tool import convert_story_to_excel

def story_agent(state: AgentState) -> AgentState:
    try:
        # 1. Get idea analysis result from previous agent
        story_idea = state.get("idea_analysis_result", "")

        # 2. Generate story plan using LLM tool (returns structured JSON)
        story_response = story_tool.invoke({
            "idea_analysis_result": story_idea
        })

        # 3. Store structured task breakdown in state
        state["story_json"] = story_response

        # 4. Export to Excel and upload
        json_status = convert_story_to_excel.invoke({
            "story_json": story_response,
            "product_title": state.get("product_title", "untitled_project")
        })
        state["story_excel_status"] = json_status

        # 5. Update agent state tracking
        state["current_agent"] = "allocator_agent" 
        print("✅ story_agent completed — JSON size:", len(story_response))

    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
        print("❌ story_agent error:", e)

    return state

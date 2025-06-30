from app.agentstate.agent_state import AgentState
from app.tools.story_tool import story_tool
from app.tools.csv_excel_tool import convert_story_to_excel


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




'''from app.agentstate.agent_state import AgentState
from app.tools.story_tool import story_tool
from app.tools.csv_excel_tool import convert_story_to_excel

def story_agent(state: AgentState) -> AgentState:
    try:
        story_idea = state.get("idea_analysis_result", "")


        response = story_tool.invoke({
            "idea_analysis_result": story_idea})
        state["story_markdown"] = response
        
        # 3. Call the Excel conversion tool and store the result/status
        excel_status = convert_story_to_excel.invoke(state)
        state["story_excel_status"] = excel_status
        
        state["current_agent"] = "next_agent" 

    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"

    return state



'''
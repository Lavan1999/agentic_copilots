from app.agentstate.agent_state import AgentState
from app.tools.idea_tool import idea_analysis_tool


def idea_agent(state: AgentState) -> AgentState:
    try:
        product_idea = state.get("product_idea", "")
        rag_text = state.get("rag_text", "")

        response = idea_analysis_tool.invoke({
            "product_idea": product_idea,
            "rag_text": rag_text
        })

        state["idea_analysis_result"] = response
        state["current_agent"] = "story_agent" 
        print("🧠 idea_agent response:", response)



    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"

    return state

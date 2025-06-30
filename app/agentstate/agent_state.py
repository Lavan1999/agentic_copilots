from typing import TypedDict, Optional, List

class AgentState(TypedDict, total=False):
    product_title: str
    product_idea: str
    rag_text: Optional[str]

    # Store full JSON or markdown from idea agent
    idea_analysis_result: Optional[str]

    # Store full JSON or markdown from story agent
    story_generation_result: Optional[str]

    # You can add further agent results here later (epic_agent, dev_plan_agent, etc.)

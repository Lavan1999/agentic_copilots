from langchain_core.tools import tool
from app.model.llm import llm
from langchain_core.prompts import PromptTemplate

@tool
def story_tool(idea_analysis_result: str) -> list:
    """
    Generate a 30-day Agile task plan in structured JSON format.
    """
    prompt = PromptTemplate.from_template("""
    You are a senior project manager AI. You will receive a product concept and idea analysis. Based on this, generate a 30-day implementation plan for three developer types:

    - Frontend Developer
    - Backend Developer
    - AI/Automation Developer

    For each day and developer, output:
    - Serial number (S.No)
    - Developer type
    - Day (e.g., Day 1)
    - Task description
    - Estimated effort (1–10)
    - Skills required (list)

    Return only JSON. Format example:

    ```json
    [
      {
        "S.No": 1,
        "Developer Type": "Frontend",
        "Day": "Day 1",
        "Task Description": "Design login UI in Figma",
        "Estimated Effort": 4,
        "Skills Required": ["Figma", "React"]
      },
      {
        "S.No": 2,
        "Developer Type": "Backend",
        "Day": "Day 1",
        "Task Description": "Set up Express server",
        "Estimated Effort": 5,
        "Skills Required": ["Node.js", "Express"]
      }
    ]
    ```

    Product Analysis:
    {idea_analysis_result}
    """)

    response = llm.invoke(prompt.format_prompt(idea_analysis_result=idea_analysis_result))
    response_text = response.content if hasattr(response, "content") else str(response)

    try:
        import json
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("⚠️ Could not parse response as JSON:", response_text)
        return []

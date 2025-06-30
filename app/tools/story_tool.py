from langchain_core.tools import tool
from app.model.llm import llm
from typing import Optional
from langchain_core.prompts import PromptTemplate
@tool
def story_tool(idea_analysis_result: str) -> str:
    """
    Analyze a vague product idea and extract structured insights using LLM.
    """

    prompt = PromptTemplate.from_template("""
    You are a senior project manager. You will receive a product concept and idea analysis. Based on this, generate a 15-day implementation plan, divided into tasks for three developer types:

    - Frontend Developer
    - Backend Developer
    - AI/Automation Developer

    For each day, list:
    1. A specific technical task
    2. The developer type responsible
    3. The sequence (S.No)

    The output should be a table with the following columns:
    - S.No
    - Developer Type
    - Day (e.g., Day 1, Day 2, etc.)
    - Task Description

    Be technically specific. For example:
    - Frontend: components, pages, personas
    - Backend: logic, APIs, DB schema, dependencies
    - AI: what to automate, how, which model/tool, inference flow

    Return only the table in Markdown format.

    ### Example

    | S.No | Developer Type | Day   | Task Description                                                 |
    |------|----------------|--------|------------------------------------------------------------------|
    | 1    | Frontend       | Day 1 | Design wireframe for voice check-in page                         |
    | 2    | Backend        | Day 1 | Define PostgreSQL schema for updates, blockers, and users        |
    | 3    | AI             | Day 1 | Evaluate Whisper and Google STT APIs for transcription           |
    | 4    | Frontend       | Day 2 | Build React component for audio recording and playback           |
    | 5    | Backend        | Day 2 | Set up FastAPI endpoint to store check-ins in database           |
    | 6    | AI             | Day 2 | Create transcription microservice using selected STT API         |

    Use the following idea analysis:

    {idea_analysis_result}

    Now return a **full 30-day table** continuing the above format and logic. Each developer type should have a complete set of technical tasks for 15 days.
    Return only a markdown table with the following columns:
    | S.No | Developer Type | Day | Task Description |
    """)

    
    response = llm.invoke(prompt)
    response = response.content if hasattr(response, "content") else str(response)
    print("response:", response)
    return response



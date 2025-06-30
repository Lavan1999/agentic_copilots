
from langchain_core.tools import tool
from app.model.llm import llm
from langchain_core.prompts import PromptTemplate
from typing import List, Dict
from db.chroma_utils import get_similar_team_profiles
import json

@tool
def story_allocator_tool(story_json: List[Dict], team_metadata: Dict, product_title: str) -> List[Dict]:
    """
    Uses LLM to allocate tasks from story_json to team members based on skills, metadata, and historical vector DB.
    """
    enriched_history = {}

    for dev in team_metadata.get("team_members", []):
        examples = []
        for story in story_json:
            matches = get_similar_team_profiles(
                query=story["Task Description"],
                dev_name=dev["name"],
                product_title=product_title,
                k=3
            )
            if matches:
                examples.append({
                    "story": story["Task Description"],
                    "matches": matches
                })
        enriched_history[dev["name"]] = {
            "past_matches": examples,
            "email": dev.get("email", "not_provided@example.com"),
            "skills": dev.get("skills", []),
            "role": dev.get("role", "")
        }

    prompt = PromptTemplate.from_template("""
You are an AI Team Allocator. Your job is to assign software tasks to developers using three sources of truth:

1. A list of structured tasks (stories)
2. Metadata about the team (skills, roles, email, availability)
3. Past work history (from a knowledge base of previous tasks done by the team)

Your goal is to assign each task to the best-suited developer using skills + domain similarity + past task examples.

### INPUT
Stories:
{story_json}

Team Metadata:
{team_metadata}

Historical Matches from Vector DB:
{enriched_history}

### OUTPUT
Return only JSON in this format:
[
  {
    "story_id": 3,
    "title": "Build login API",
    "assigned_to": "Karan",
    "match_score": 4,
    "matched_domains": ["Auth", "REST API"],
    "email": "karan@devs.com"
  },
  ...
]
""")

    formatted_prompt = prompt.format_prompt(
        story_json=json.dumps(story_json, indent=2),
        team_metadata=json.dumps(team_metadata, indent=2),
        enriched_history=json.dumps(enriched_history, indent=2)
    )

    response = llm.invoke(formatted_prompt)
    response_text = response.content if hasattr(response, "content") else str(response)

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print("⚠️ Could not parse response as JSON:", response_text)
        return []


'''from langchain_core.tools import tool
from app.agentstate.agent_state import AgentState

@tool
def story_allocator_tool(state: AgentState) -> AgentState:
    """
    Tool for assigning user stories to developers based on skills and availability.
    """
    story_data = state.story_json or []
    team = state.team_metadata.get("team_members", [])

    allocations = []
    team_availability = {dev["name"]: dev["availability"] for dev in team}

    for story in story_data:
        best_match = None
        highest_score = 0

        for dev in team:
            skill_overlap = len(set(dev["skills"]) & set(story.get("skills_required", [])))
            if skill_overlap > highest_score and team_availability[dev["name"]] > 0:
                best_match = dev
                highest_score = skill_overlap

        if best_match:
            allocations.append({
                "story_id": story.get("id"),
                "title": story.get("title"),
                "assigned_to": best_match["name"],
                "skills_matched": highest_score
            })
            team_availability[best_match["name"]] -= story.get("estimated_effort", 5)
        else:
            allocations.append({
                "story_id": story.get("id"),
                "title": story.get("title"),
                "assigned_to": "Unassigned",
                "skills_matched": 0
            })

    state.story_allocations = allocations
    return state
'''
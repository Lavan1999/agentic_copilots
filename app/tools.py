from langchain_core.tools import tool
from app.model.llm import llm
from typing import Optional

@tool
def idea_analysis_tool(product_idea: str, rag_text: Optional[str] = "") -> str:
    """
    Analyze a vague product idea and extract structured insights using LLM.
    """
    prompt = f"""
You are a Senior Product Strategy AI and Product Idea Analyst with deep expertise in interpreting vague product ideas across industries such as SaaS, HealthTech, EdTech, IoT, and FinTech.

Your role is foundational in an autonomous Agile execution system — your structured insights will directly fuel downstream agents responsible for epics, sprint planning, developer allocation, and stakeholder communication.

---

## 🎯 Your Mission:

Given a raw product idea and optional Agile documentation (RAG), perform a **deep, structured analysis** of the product from a product management, user experience, and technical feasibility perspective.
Your mission is to extract:
- domain
- features
- modules
- personas
- use_case_map
- risks
- constraints
---

## 📌 Goals:

1. Identify the **domain and scope** of the product idea.
2. Break down the product into **key features** and **functional modules**.
3. Infer **target personas** and describe their **goals and pain points**.
4. Create a **use-case map** (how personas interact with the system end-to-end).
5. Identify **technical, legal, or strategic risks** and **constraints**.
6. Leverage Agile documentation or prior knowledge (RAG) to enrich the output with best practices or references.

---

## 🧾 Output Format:

Provide a structured response in either **Markdown** or **JSON** format with the following fields:

- `domain`
- `features`
- `modules`
- `personas`
- `use_case_map`
- `risks`
- `constraints`
- `rag_enhancements` (leave empty if no RAG was provided)


using this product idea:
\n{product_idea}\n\n
Additional Agile Documentation:
\n{rag_text}

Output your analysis in Markdown format with labeled sections.
"""
    response = llm.invoke(prompt)
    response = response.content if hasattr(response, "content") else str(response)
    print("response:", response)
    return response




def rag_feature_enhancer(product_idea: str) -> str:
    idea = product_idea.lower()

    if any(keyword in idea for keyword in ["health", "wearable", "remote monitoring"]):
        return (
            "RAG Insights:\n"
            "- Domain: HealthTech\n"
            "- Use Case: Real-time remote patient monitoring\n"
            "- Typical Modules: Sensor integration, Health dashboard, Alert engine, Compliance tracker\n"
            "- Risks: HIPAA/GDPR compliance, device calibration, user adoption\n"
            "- Similar Products: Fitbit, Oura, Apple Health\n"
        )
    elif any(k in idea for k in ["education", "learning", "students"]):
        return (
            "RAG Insights:\n"
            "- Domain: EdTech\n"
            "- Use Case: Personalized learning with analytics\n"
            "- Typical Modules: LMS, AI tutor, Assessment engine, Dashboard\n"
            "- Risks: Accuracy, engagement, accessibility\n"
            "- Similar Products: Byju’s, Khan Academy\n"
        )
    elif any(k in idea for k in ["finance", "investment"]):
        return (
            "RAG Insights:\n"
            "- Domain: FinTech\n"
            "- Use Case: Automated finance management\n"
            "- Modules: Aggregator, Budget tool, Robo-advisor\n"
            "- Risks: Data security, compliance\n"
            "- Products: Mint, Robinhood\n"
        )
    elif any(k in idea for k in ["project", "team", "collaboration"]):
        return (
            "RAG Insights:\n"
            "- Domain: SaaS\n"
            "- Use Case: Team collaboration\n"
            "- Modules: Task board, Chat, Calendar\n"
            "- Risks: Slack/Teams dependency\n"
            "- Products: Asana, Notion\n"
        )
    else:
        return (
            "RAG Insights:\n"
            "- Domain: Generic SaaS\n"
            "- Use Case: Workflow automation\n"
            "- Modules: Auth, Dashboard, Role mgmt\n"
            "- Risks: MVP scope, scale bottlenecks\n"
        )
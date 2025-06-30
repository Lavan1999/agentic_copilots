from langchain_core.tools import tool
from app.model.llm import llm
from typing import Optional
from langchain_core.prompts import PromptTemplate
@tool
def idea_analysis_tool(product_idea: str, rag_text: Optional[str] = "") -> str:
    """
    Analyze a vague product idea and extract structured insights using LLM.
    """
    prompt = PromptTemplate.from_template("""
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
""")
    response = llm.invoke(prompt)
    response = response.content if hasattr(response, "content") else str(response)
    print("response:", response)
    return response




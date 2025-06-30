from langchain_core.tools import tool
from app.model.llm import llm
from typing import Optional
from langchain_core.prompts import PromptTemplate
from db.chroma_utils import load_rag_knowledge

@tool
def idea_analysis_tool(product_idea: str, product_title: str, rag_text: Optional[str] = "") -> str:
    """
    Analyze a vague product idea with optional RAG context pulled from ChromaDB if rag_text is present.
    """
    enriched_rag = ""
    if rag_text and product_title:
        try:
            enriched_rag = load_rag_knowledge(product_title=product_title, query=product_idea, k=5)
        except Exception as e:
            enriched_rag = ""
            print(f"⚠️ Failed to load RAG from ChromaDB: {e}")

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

---

Product Idea:
{product_idea}

RAG Knowledge Base:
{enriched_rag}
""")

    response = llm.invoke(prompt.format_prompt(product_idea=product_idea, enriched_rag=enriched_rag))
    return response.content if hasattr(response, "content") else str(response)

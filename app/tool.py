
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
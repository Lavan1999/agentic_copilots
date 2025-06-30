import streamlit as st
import json
import fitz  
from db.mongo_utils import save_product_idea 
from app.agentstate.agent_state import AgentState
from langgraph_flow import build_app
from db.chroma_utils import store_excel_to_chroma
from db.chroma_utils import store_rag_to_chroma
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def run_idea_analysis(product_idea: str, rag_text: str = ""):
    """Run the idea analysis workflow"""
    app = build_app()

    initial_state = AgentState(
        product_title=product_idea.strip()[:30].replace(" ", "_"),
        product_idea=product_idea,
        rag_text=rag_text,
        idea_analysis_result="",
        story_markdown="",
        story_excel_status=""
    )

    try:
        final_state = app.invoke(initial_state)

        print("\n" + "=" * 60)
        print("✅ IDEA ANALYSIS COMPLETED")
        print("=" * 60)
        print(f"\n📌 RESULT:\n{final_state['idea_analysis_result']}")
        
        
        # print("\n" + "=" * 60)
        # print("✅ STORY PLANNER COMPLETED")
        # print("=" * 60)
        # print(f"\n📌 RESULT:\n{final_state['story_markdown']}")
        return final_state


    except Exception as e:
        print(f"\n💥 Idea analysis workflow failed: {str(e)}")
        return None


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="Agentic AI Co-Pilot", layout="wide")
st.title("🚀 Agentic AI Co-Pilot for Agile Project Execution")
st.subheader("Turn a vague product idea + team metadata into an autonomous sprint plan")

# Title, product idea
product_title = st.text_input("Enter a short title for your product idea", placeholder="e.g., Remote Health Tracker")
product_idea = st.text_area(
    "🧠 Describe your idea vaguely, and let AI do the rest!",
    placeholder="A wearable for monitoring elderly patients remotely using health sensors...",
    height=180
)


# Optional RAG File Upload
st.markdown("### 📄 Upload Agile Docs / Playbook (Optional)")
uploaded_file = st.file_uploader("Upload `.txt`, `.md`, or `.pdf`:", type=["txt", "md", "pdf"], key="rag")

rag_text = None
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    try:
        if file_type in ["txt", "md"]:
            rag_text = uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                rag_text = "\n".join(page.get_text() for page in doc)

        if rag_text:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            with st.expander("📘 View Extracted RAG Text"):
                st.text_area("RAG Content", rag_text, height=250)

            try:
                store_rag_to_chroma(rag_text, product_title.strip())
                st.success("📚 RAG content indexed into ChromaDB")
            except Exception as e:
                st.error(f"❌ Failed to store RAG content in ChromaDB: {e}")

    except Exception as e:
        st.error(f"Failed to extract file: {e}")


# Team Metadata
default_team = {
    "team_name": "Velocity Devs",
    "team_members": [
        {"name": "Riya", "role": "Frontend Developer", "skills": ["React", "TypeScript", "Figma"], "availability": 25},
        {"name": "Karan", "role": "Backend Developer", "skills": ["Node.js", "MongoDB", "Express"], "availability": 30},
        {"name": "Sneha", "role": "AI/ML Engineer", "skills": ["Python", "Whisper", "LLMs", "FastAPI"], "availability": 20},
        {"name": "Vikram", "role": "DevOps Engineer", "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"], "availability": 15}
    ]
}
st.markdown("### 👥 Team Metadata (JSON Format)")
team_metadata_input = st.text_area("Paste your team metadata:", value=json.dumps(default_team, indent=2), height=300)


st.markdown("### 📊 Upload Team Historical Data (Excel)")
team_history_file = st.file_uploader("Upload team task history Excel:", type=["xlsx", "xls"])

if team_history_file:
    df_preview = pd.read_excel(team_history_file)
    st.markdown("#### 🔍 Preview of Uploaded Excel")
    st.dataframe(df_preview.head(10))

    required_cols = {"Developer", "Task Description"}
    if not required_cols.issubset(df_preview.columns):
        st.error("❌ Excel must contain columns: 'Developer', 'Task Description'")
    elif product_title.strip():
        try:
            store_excel_to_chroma(team_history_file, namespace=product_title.strip())
            st.success("✅ Historical data saved to ChromaDB")
        except Exception as e:
            st.error(f"❌ Failed to load into ChromaDB: {e}")



# Process Button
if st.button("✨ Run Agentic Planner"):
    if not product_title.strip() or not product_idea.strip():
        st.warning("🚨 Title and product idea are required.")
    else:
        try:
            # Parse JSON
            team_metadata = json.loads(team_metadata_input)

            # ✅ Save to MongoDB
            doc_id = save_product_idea(
                title=product_title,
                product_idea=product_idea,
                rag_text=rag_text,
                team_metadata=team_metadata
            )
            st.success(f"✅ Product idea saved to MongoDB (ID: {doc_id})")

            # ✅ Run LangGraph Agent
            with st.spinner("🤖 Running LangGraph agent..."):
                result = run_idea_analysis(product_idea=product_idea, rag_text=rag_text or "")

            st.success("🎉 First Agentic workflow complete!")
            #st.markdown("### 🔍 First Agent Output")
            st.markdown(result["idea_analysis_result"])
            
            # st.success("🎉 Story Agentic workflow complete!")
            # st.markdown("### 🔍 Story Agent Output")
            # st.markdown("### ✍️ Story Task Breakdown")

        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format in team metadata.")
        except Exception as e:
            st.error(f"🚨 Something went wrong: {e}")


'''# Optional RAG File Upload
st.markdown("### 📄 Upload Agile Docs / Playbook (Optional)")
uploaded_file = st.file_uploader("Upload `.txt`, `.md`, or `.pdf`:", type=["txt", "md", "pdf"])

rag_text = None
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    try:
        if file_type in ["txt", "md"]:
            rag_text = uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                rag_text = "\n".join(page.get_text() for page in doc)
        if rag_text:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            with st.expander("📘 View Extracted RAG Text"):
                st.text_area("RAG Content", rag_text, height=250)
    except Exception as e:
        st.error(f"Failed to extract file: {e}")'''



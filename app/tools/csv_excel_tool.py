import pandas as pd
import io
from langchain.tools import tool
from db.mongo_utils import story_file_upload  # assumed utility function
from bson.binary import Binary

def markdown_table_to_df(markdown: str) -> pd.DataFrame:
    lines = [line for line in markdown.strip().split('\n') if '|' in line]
    cleaned_csv = '\n'.join([line.replace('|', ',').strip(', ') for line in lines])
    return pd.read_csv(io.StringIO(cleaned_csv), skiprows=1)

@tool
def convert_story_to_excel(agent_state: dict) -> str:
    """
    Converts the story_markdown from AgentState into an Excel file using the product_title as filename,
    and uploads the file to MongoDB.
    """
    try:
        product_title = agent_state.get("product_title", "untitled_project").replace(" ", "_")
        story_markdown = agent_state.get("story_markdown", "")
        
        if not story_markdown:
            return "❌ story_markdown is missing in AgentState."
        
        # Convert to DataFrame
        df = markdown_table_to_df(story_markdown)
        
        # Create Excel file in memory
        filename = f"{product_title}_task_splitup.xlsx"
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        
        # Upload to MongoDB
        upload_result = story_file_upload(
            filename=filename,
            content=Binary(excel_buffer.getvalue()),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        return f"✅ Excel saved and uploaded as '{filename}' with {len(df)} tasks."

    except Exception as e:
        return f"❌ Error during Excel export or upload: {str(e)}"



"""import pandas as pd
import io
import response


# Step 1: Replace markdown symbols to make it CSV-readable
markdown_table = response.strip()  # ← Replace with your actual response

# Step 2: Convert markdown to a format pandas can read
cleaned_data = markdown_table.replace('|', ',').replace(',,', '\n')
df = pd.read_csv(io.StringIO(cleaned_data), skiprows=1)

# Optional: Clean column names
df.columns = [col.strip() for col in df.columns]

# Step 3: Save to Excel
df.to_excel("task_splitup.xlsx", index=False)

print("✅ Task_splitup.xlsx files saved.")

from langchain.tools import tool

@tool
def convert_markdown_to_excel(markdown_str: str, filename: str = "task_splitup.xlsx") -> str:
    df = markdown_table_to_df(markdown_str)
    df.to_excel(filename, index=False)
    return f"Excel saved as {filename}"""
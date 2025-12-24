import os
import json
from dotenv import load_dotenv
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from vespa.application import Vespa  # Ensure you have 'pyvespa' installed

load_dotenv()

from vespa.application import Vespa

# Path to your security files

app = Vespa(
    url=os.getenv("VESPA_ENDPOINT"),
    cert="/Users/shivamjogdand/Desktop/Learning/DeepAgents/Report_Generation_Git/Report_Generation/certs/public.pem",
    key="/Users/shivamjogdand/Desktop/Learning/DeepAgents/Report_Generation_Git/Report_Generation/certs/private.pem"
)

@tool
def execute_vespa_yql(yql_query: str):
    """
    Executes a YQL query against the Vespa AI 'pefund' index.
    Input should be a valid YQL string.
    Returns the 'hits' from the search results.
    """
    try:
        query = {"yql": yql_query}
        result = app.query(body=query)
        # Return only the relevant fields to save context window space
        return [hit['fields'] for hit in result.hits]
    except Exception as e:
        return f"Error executing Vespa query: {str(e)}"

# --- STEP 2: Setup FileSystemBackend ---
working_dir = os.path.join(os.getcwd(), "agent_workspace")
os.makedirs(working_dir, exist_ok=True)
# Ensure the skills directory exists
os.makedirs(os.path.join(working_dir, "skills", "vespa_search"), exist_ok=True)

fs_backend = FilesystemBackend(root_dir=working_dir, virtual_mode=True)

# --- STEP 3: Define Advanced Skill Protocol ---
SKILL_INSTRUCTION = """
You are a Deep Agent with access to a local filesystem and external database tools.
LOCATION: Your skills are in './skills/'.

PROTOCOL:
1. EXPLORE: 'ls' on './skills' to find capabilities.
2. PEEK: For a relevant folder, use 'read_file' on 'SKILL.md' but only focus on the YAML frontmatter.
3. LOAD: If the 'description' in the YAML matches the user's request, read the FULL 'SKILL.md' and follow its specific instructions. 
4. QUERY: Use 'execute_vespa_yql' based on the YQL patterns found in SKILL.md.
5. STORAGE: Save final summarized findings as a .md file in the root workspace.
"""

# --- STEP 4: Initialize LLM & Agent ---
llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview", # Using the latest stable pro model
    temperature=0.2,        # Lower temperature for better YQL generation
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Combine Filesystem tools with our Vespa tool
agent_tools = [execute_vespa_yql]

agent_executor = create_deep_agent(
    model=llm,
    backend=fs_backend, 
    tools=agent_tools,
    system_prompt=f"You are a Financial Analyst agent.\n{SKILL_INSTRUCTION}"
)

# --- STEP 5: Execution ---
config = {"configurable": {"thread_id": "vespa_research_001"}}

# Example query requiring the agent to use the tenant ID you provided earlier
user_task = (
    "Search for company data for tenant '90da21d0-8e83-4e84-961b-e6fec8b9dafe' "
    "Summarize the overall findings as per financial analysis report and save it to a file named 'phonepe_report.md'."
)

user_input = {"messages": [("user", user_task)]}

print("--- Starting Agent Workflow ---")
for chunk in agent_executor.stream(user_input, config):
    # This prints the thought process and tool calls (ls -> read_file -> execute_vespa_yql -> write_file)
    print(chunk)
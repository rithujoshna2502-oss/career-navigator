import os
import sys
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. FIX: Force UTF-8 encoding for Windows terminals to prevent 'charmap' errors
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 2. Configuration
# Replace these with your actual keys
os.environ["OPENROUTER_API_KEY"] = "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" 
os.environ["SERPER_API_KEY"] = "8901c3ae8e48810b721c0e71c01d386dfe38b458"

# 3. FIX: Initialize the LLM with the correct 2025 provider prefix
openrouter_llm = LLM(
    model="openrouter/mistralai/mistral-7b-instruct", 
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    extra_headers={
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "Career Navigator"
    }
)

# 4. Define Agents
market_insight_agent = Agent(
    role='Real-Time Job Market Analyst',
    goal='Identify trending skills for AI Engineers in 2025.',
    backstory='Expert analyst for live market trends.',
    tools=[SerperDevTool()],
    llm=openrouter_llm,
    verbose=True # FIX: Must be a boolean True/False, not a number
)

career_strategist = Agent(
    role='Career Strategist',
    goal='Develop a 3-month roadmap based on identified skills.',
    backstory='Expert at turning market data into actionable learning plans.',
    llm=openrouter_llm,
    verbose=True
)

# 5. Define Tasks
job_market_analysis_task = Task(
    description="Analyze current top 5 skills for AI Engineers in 2025.",
    expected_output="A bulleted list of 5 trending skills and their frequency.",
    agent=market_insight_agent
)

strategy_planning_task = Task(
    description="Create a 3-month roadmap using the skills found in the market analysis.",
    expected_output="A month-by-month learning plan with specific project ideas.",
    agent=career_strategist,
    context=[job_market_analysis_task]
)

# 6. Build and Run the Crew
career_navigator_crew = Crew(
    agents=[market_insight_agent, career_strategist],
    tasks=[job_market_analysis_task, strategy_planning_task],
    process=Process.sequential,
    verbose=True # FIX: Must be a boolean True/False
)

print("########################")
print("## Starting Career Navigator Analysis")
print("########################")

try:
    result = career_navigator_crew.kickoff()
    print("\n\n########################")
    print("## FINAL RESULT")
    print("########################")
    print(result)
except Exception as e:
    print(f"An error occurred during execution: {e}")


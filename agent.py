# agent.py
# AI Agent Example using Azure OpenAI + CrewAI (via LiteLLM)
# Author: Sean Breeden

from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
import sys

load_dotenv()

API_KEY     = os.environ["AZURE_OPENAI_API_KEY"]
ENDPOINT    = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]
DEPLOYMENT  = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]

llm = LLM(
    model=f"azure/{DEPLOYMENT}",
    api_key=API_KEY,
    api_base=ENDPOINT,
    api_version=API_VERSION,
    temperature=0.3,
)

ceo = Agent(
    role="Founder/CEO",
    goal="Define a sharp go-to-market direction for a new product.",
    backstory="Pragmatic startup CEO who loves concise, high-leverage plans.",
    allow_delegation=True,
    llm=llm,
)

marketer = Agent(
    role="Marketing Lead",
    goal="Create a punchy, conversion-focused launch plan.",
    backstory="Lifecycle & growth marketer obsessed with clear messaging.",
    allow_delegation=False,
    llm=llm,
)

launch_task = Task(
    description=(
        "Given the product: '{product}', create a 7-point launch plan with:\n"
        "1) One-sentence value prop\n"
        "2) ICP bullets x 3\n"
        "3) Core message\n"
        "4) Channels (3-5) with why\n"
        "5) 2-week content calendar (table)\n"
        "6) Simple KPI targets\n"
        "7) One scrappy experiment"
    ),
    expected_output="A tight Markdown doc that a team could execute immediately.",
    agent=marketer
)

crew = Crew(
    agents=[ceo, marketer],
    tasks=[launch_task],
    process=Process.hierarchical,
    manager_llm=llm,
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={"product": "Retro T-shirt website"})
    print(result)

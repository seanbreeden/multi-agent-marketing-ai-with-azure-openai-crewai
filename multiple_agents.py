# multiple_agents.py
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

# add a developer
developer = Agent(
  role="Full-stack Developer with senior developer knowledge of React JS",
  goal="Turn the plan into a technical spec + repo structure.",
  backstory="Software developer with extensive experience developing React websites",
  allow_delegation=False,
  llm=llm,
)

# developer task: develop site
spec_task = Task(
  description=(
    "From the launch plan, produce a short technical spec: "
    "APIs, data schema, minimal architecture, and a repo scaffold (tree)."
  ),
  expected_output="Markdown spec with a code-block repo tree.",
  agent=developer,
)

# ceo task: qa
qa_task = Task(
  description=(
    "Review the plan and spec and list the top 7 risks with mitigations."
  ),
  expected_output="Bulleted risk register with owners and due dates.",
  agent=ceo,
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

# define the team
crew = Crew(
                         #v add the extra agent here
  agents=[ceo, marketer, developer],
                      #v add the extra developer and ceo task here
  tasks=[launch_task, spec_task, qa_task],
  process=Process.hierarchical,
  manager_llm=llm,
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={"product": "Retro T-shirt website"})
    print(result)

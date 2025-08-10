```
      ______   ______                                                 __
     /      \ |      \                                               |  \
    |  $$$$$$\ \$$$$$$        ______    ______    ______   _______  _| $$_
    | $$__| $$  | $$         |      \  /      \  /      \ |       \|   $$ \
    | $$    $$  | $$          \$$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\\$$$$$$
    | $$$$$$$$  | $$         /      $$| $$  | $$| $$    $$| $$  | $$ | $$ __
    | $$  | $$ _| $$_       |  $$$$$$$| $$__| $$| $$$$$$$$| $$  | $$ | $$|  \
    | $$  | $$|   $$ \       \$$    $$ \$$    $$ \$$     \| $$  | $$  \$$  $$
     \$$   \$$ \$$$$$$        \$$$$$$$ _\$$$$$$$  \$$$$$$$ \$$   \$$   \$$$$
                                      |  \__| $$
                                       \$$    $$
                                        \$$$$$$
                                                          __
                                                         |  \
      ______   __    __  ______   ______ ____    ______  | $$  ______
     /      \ |  \  /  \|      \ |      \    \  /      \ | $$ /      \
    |  $$$$$$\ \$$\/  $$ \$$$$$$\| $$$$$$\$$$$\|  $$$$$$\| $$|  $$$$$$\
    | $$    $$  >$$  $$ /      $$| $$ | $$ | $$| $$  | $$| $$| $$    $$
    | $$$$$$$$ /  $$$$\|  $$$$$$$| $$ | $$ | $$| $$__/ $$| $$| $$$$$$$$
     \$$     \|  $$ \$$\\$$    $$| $$ | $$ | $$| $$    $$| $$ \$$     \
      \$$$$$$$ \$$   \$$ \$$$$$$$ \$$  \$$  \$$| $$$$$$$  \$$  \$$$$$$$
                                               | $$
                                               | $$
                                                \$$
```

Blog post: https://www.seanbreeden.com/blog/multi-agent-marketing-ai-with-azure-openai-crewai

**Using Azure OpenAI + CrewAI (via LiteLLM)**

AI-Powered Multi-Agent Marketing Planner that simulates a two-person marketing team—CEO (strategy) + Marketing Lead (execution) to generate a complete, execution-ready 7-step product launch plan from a single product name. Built with CrewAI (multi-agent orchestration) and Azure OpenAI (enterprise LLM) via LiteLLM's Azure adapter.

## Features

- **Multi-agent workflow**: A CEO agent defines the go-to-market (GTM) direction, and a Marketing Lead agent translates it into a tactical plan
- **Deterministic output shape**: The plan includes a one-sentence value proposition, ICP bullets, a core message, channels, a 2-week content calendar (in a table), key performance indicators (KPIs), and one "scrappy" experiment
- **Azure-first**: The application exclusively calls your Azure OpenAI deployment, not public OpenAI endpoints
- **Single-file runnable**: The `agent.py` script produces a full Markdown plan to standard output

## Architecture

**CrewAI** orchestrates agents and tasks, and calls an LLM through LiteLLM.

**LiteLLM (Azure adapter)** normalizes API differences and constructs the correct Azure chat completions route.

**Azure OpenAI** hosts your GPT models; you provide the endpoint, API version, and deployment name.

```
[User/Product Name] → CrewAI (Agents/Task) → LiteLLM (azure/*) → Azure OpenAI → Markdown Launch Plan
```

## Prerequisites

- **Python 3.12** (recommended)
- An **Azure OpenAI resource** with a chat deployment (e.g., a GPT-4o family model)
- The following Python packages:
  - `crewai==0.157.0`
  - `openai==1.99.6`
  - `langchain-openai==0.3.29`
  - `python-dotenv`

## Quick Start

### 1. Clone the repository and create a virtual environment

```bash
git clone <your-repo-url> ai-agent
cd ai-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install crewai==0.157.0 openai==1.99.6 langchain-openai==0.3.29 python-dotenv
```

### 2. Configure your environment

Create a `.env` file in the project root with your Azure OpenAI credentials:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-07-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1  # EXACT deployment name in Azure
```

**Important Notes:**
- `AZURE_OPENAI_ENDPOINT` must **not** include `/openai`
- `AZURE_OPENAI_DEPLOYMENT_NAME` is the name you gave your deployment, not the model family

### 3. Run the script

```bash
python agent.py
```

You'll be prompted to enter a product name (or the script will use a default). A complete, ready-to-execute Markdown plan will then be printed to standard output.

## Example Output

```markdown
# Launch Plan: AI-powered retro T-shirt designer

**Value Prop (1 sentence):** Design & sell retro-inspired tees in minutes using AI-assisted workflows.

**ICP (3 bullets):**
- Indie apparel founders needing fast concept-to-storefront
- Shopify/Magento merchants testing new SKUs weekly
- Designers seeking AI co-creation for 70s/80s aesthetics

**Core Message:** "Turn retro ideas into shippable SKUs—today."

**Channels (why):**
1. Email (owned audience, highest ROI)
2. Instagram Reels (visual, style-driven discovery)
3. Reddit niche subs (retro/collectibles—contextual demand)
...
```

## Project Structure

```
├─ agent.py         # Main script: agents, tasks, Crew, Azure LLM config
├─ .env             # Your secrets
└─ README.md        # This file
```

## Configuration

In `agent.py`, the LLM object is configured to use Azure:

```python
from crewai import Agent, Task, Crew, Process, LLM
# ...
llm = LLM(
    model=f"azure/{DEPLOYMENT}",          # azure/<your-deployment-name>
    api_key=API_KEY,                      # AZURE_OPENAI_API_KEY
    api_base=ENDPOINT,                    # https://<resource>.openai.azure.com (NO /openai)
    api_version=API_VERSION,              # e.g., 2024-07-01
    temperature=0.3,
)
```

CrewAI then uses this Azure-configured LLM for both agents and the manager.

## Troubleshooting

### 404 Resource not found

**Cause:** Wrong path or deployment name.

**Fix:**
- Ensure `api_base` is the resource root (e.g., `https://<resource>.openai.azure.com`), **not** `.../openai`
- Verify `AZURE_OPENAI_DEPLOYMENT_NAME` is the exact deployment name from your Azure portal
- Confirm `AZURE_OPENAI_API_VERSION` is supported by your deployment (e.g., `2024-06-01` is generally fine for the GPT-4o family)

### "The api_key client option must be set..."

**Cause:** The script tried to use a non-Azure OpenAI endpoint instead of Azure.

**Fix:**
- Make sure you're constructing the LLM object with `model=f"azure/{DEPLOYMENT}"`
- Unset any stray environment variables like `OPENAI_API_KEY`, `OPENAI_BASE_URL`, or `OPENAI_PROJECT`

### Still having problems?

Enable verbose logging to see the exact requests being made:

```bash
export LITELLM_LOG=DEBUG
python agent.py
```

You should see requests like this:
```
https://<resource>.openai.azure.com/openai/deployments/<DEPLOYMENT>/chat/completions?api-version=2024-07-01
```

If you see `/openai/openai/` or a different deployment name, you'll know where to fix `api_base` or `DEPLOYMENT`.

## FAQs

**Q: Can I use LangChain's AzureChatOpenAI instead?**
A: Yes, but CrewAI v0.157.0 will still call LiteLLM under the hood for some pathways. Using CrewAI's LLM with `model="azure/<deployment>"` removes ambiguity and is the recommended approach.

**Q: Which models work?**
A: Any chat deployment you've provisioned in Azure OpenAI (e.g., GPT-4o variants). You must use the deployment name, not the model name.

**Q: How do I change temperature or token limits?**
A: Pass additional keyword arguments to the `LLM(...)` constructor, for example: `temperature=0.2`, `max_tokens=1500`.

## Development Tips

- Pin your package versions (as listed above) to ensure constructor signatures remain stable
- Never commit your `.env` file to version control!

import streamlit as st
from groq import Groq

# ============ LLM Setup ============

class LLM:
    def __init__(self, model_name, client):
        self.model_name = model_name
        self.client = client

    def generate(self, messages):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        return response.choices[0].message.content


def get_llm():
    # ✅ अपनी API Key यहां डालो
    api_key = "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"  # <-- इसे अपनी असली API key से replace करना
    return Groq(api_key=api_key)

# ============ Agent Setup ============

class Agent:
    def __init__(self, name, role, goal, backstory, tools, llm):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.llm = llm

    def execute(self, task):
        messages = [
            {"role": "system", "content": f"You are {self.name}, {self.role}. Goal: {self.goal}. Backstory: {self.backstory}"},
            {"role": "user", "content": task}
        ]
        return self.llm.generate(messages)

# ============ Task & Crew ============

class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

    def run(self):
        return self.agent.execute(self.description)


class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self):
        results = []
        for task in self.tasks:
            results.append(task.run())
        return "\n\n---\n\n".join(results)

# ============ Crew Creation ============

def create_agents():
    client = get_llm()
    llm = LLM("llama-3.3-70b-versatile", client)

    market_analyst = Agent(
        name="Market Analyst",
        role="Market Research Expert",
        goal="Analyze market demand, trends, and user pain points",
        backstory="10+ years in startup analysis across sectors.",
        tools=[],
        llm=llm
    )

    ecosystem_expert = Agent(
        name="Ecosystem Expert",
        role="Startup Ecosystem Specialist",
        goal="Evaluate existing solutions, competitors, and investor interest",
        backstory="Knows the global startup ecosystem deeply.",
        tools=[],
        llm=llm
    )

    business_strategist = Agent(
        name="Business Strategist",
        role="Business Strategy Consultant",
        goal="Suggest improvements and actionable strategies",
        backstory="MBA from Stanford and 12+ years of startup advising.",
        tools=[],
        llm=llm
    )

    investment_analyst = Agent(
        name="Investment Analyst",
        role="Venture Capital Specialist",
        goal="Analyze viability from an investor lens",
        backstory="Analyzed 500+ startups for funding and scale.",
        tools=[],
        llm=llm
    )

    return market_analyst, ecosystem_expert, business_strategist, investment_analyst


def create_tasks(market_analyst, ecosystem_expert, business_strategist, investment_analyst, startup_info):
    return [
        Task(description=f"Analyze market for startup idea: {startup_info}", agent=market_analyst),
        Task(description=f"Evaluate competitors and ecosystem for: {startup_info}", agent=ecosystem_expert),
        Task(description=f"Suggest improvements for business idea: {startup_info}", agent=business_strategist),
        Task(description=f"Assess investment potential of: {startup_info}", agent=investment_analyst)
    ]


def create_crew(agents, tasks):
    return Crew(agents=agents, tasks=tasks)

# ============ Run Function ============

def run_startup_validator(startup_info):
    try:
        market_analyst, ecosystem_expert, business_strategist, investment_analyst = create_agents()
        tasks = create_tasks(market_analyst, ecosystem_expert, business_strategist, investment_analyst, startup_info)
        crew = create_crew(
            [market_analyst, ecosystem_expert, business_strategist, investment_analyst],
            tasks
        )

        with st.spinner('Analyzing your startup idea... Please wait.'):
            result = crew.kickoff()
            return result
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# ============ Streamlit UI ============

st.set_page_config(page_title="Startup Idea Validator", layout="wide")

st.title("🚀 Startup Idea Checker: AI-Enhanced Expert Feedback in Seconds")
st.markdown("Turn your raw startup idea into a refined pitch with expert-level AI validation and guidance.")

startup_info = st.text_area("🧠 Enter your startup idea:", height=200, placeholder="Describe your idea in detail...")

if st.button("🔍 Validate Idea"):
    if startup_info.strip():
        result = run_startup_validator(startup_info)
        if result:
            st.success("✅ Validation Complete!")
            st.markdown(result)
    else:
        st.warning("Please enter a startup idea to validate.")

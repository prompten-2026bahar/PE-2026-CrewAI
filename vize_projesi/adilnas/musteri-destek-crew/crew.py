from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks


def run(sikayet: str):
    agents = create_agents()
    tasks = create_tasks(sikayet, agents)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()

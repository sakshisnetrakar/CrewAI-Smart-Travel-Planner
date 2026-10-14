"""Five-agent sequential CrewAI workflow using a local Ollama LLM."""

import os

from dotenv import load_dotenv

load_dotenv()


def run_crewai_plan(data: dict) -> str:
    """Run the CrewAI workflow. Requires CrewAI and a locally running Ollama model."""
    from crewai import Agent, Crew, LLM, Process, Task
    from travel_tools import BudgetCalculatorTool, DestinationSearchTool, HotelTransportTool, RoutingTool, WeatherTool

    llm = LLM(model=f"ollama/{os.getenv('OLLAMA_MODEL', 'llama3.2')}", base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    coordinator = Agent(role="Travel Coordinator", goal="Coordinate a safe, practical travel plan", backstory="You coordinate specialist findings and ensure every customer requirement is addressed.", llm=llm, allow_delegation=False)
    researcher = Agent(role="Destination Research Agent", goal="Find suitable experiences", backstory="You research attractions and local experiences from assigned tools.", llm=llm, tools=[DestinationSearchTool(), WeatherTool()])
    hotel_transport = Agent(role="Hotel and Transport Agent", goal="Find affordable stay and travel options", backstory="You compare accommodation and transport estimates.", llm=llm, tools=[HotelTransportTool()])
    analyst = Agent(role="Budget Analyst Agent", goal="Verify affordability and alternatives", backstory="You calculate estimated cost and flag plans over budget.", llm=llm, tools=[BudgetCalculatorTool()])
    planner = Agent(role="Itinerary Planner Agent", goal="Create a day-by-day itinerary", backstory="You transform research and budget results into a coherent schedule.", llm=llm, tools=[RoutingTool()])
    details = f"Destination: {data['destination']}; starting location: {data['starting_location']}; dates: {data['travel_dates']}; duration: {data['duration_days']} days; budget: ₹{data['budget']:,.0f}; interests: {data['interests']}."
    research_task = Task(description=f"Research this trip using your tools. {details} Include attractions, weather, and sources.", expected_output="Attractions, local experiences, weather notes, sources.", agent=researcher)
    options_task = Task(description=f"Find hotel and transport estimates using your tool. {details}", expected_output="Hotel and transport options with costs and sources.", agent=hotel_transport)
    budget_task = Task(description=f"Calculate costs and decide whether this plan meets the budget. {details}", expected_output="Budget breakdown, comparison, cheaper alternatives if needed.", agent=analyst, context=[research_task, options_task])
    itinerary_task = Task(description=f"Create day-by-day activities with routing guidance. {details}", expected_output="Daily itinerary and travel timing notes.", agent=planner, context=[research_task, options_task, budget_task])
    final_task = Task(description=f"Consolidate all task outputs into the final personalised travel plan. {details} State that tool results are mock estimates and list sources.", expected_output="Complete itinerary, choices, budget, alternatives, sources.", agent=coordinator, context=[research_task, options_task, budget_task, itinerary_task])
    return str(Crew(agents=[coordinator, researcher, hotel_transport, analyst, planner], tasks=[research_task, options_task, budget_task, itinerary_task, final_task], process=Process.sequential, verbose=False).kickoff())

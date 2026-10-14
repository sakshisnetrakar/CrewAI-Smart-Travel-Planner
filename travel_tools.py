"""Mock external-service tools for a local CrewAI prototype.

Replace each _run body with an authorised API request when credentials are available.
"""

from crewai.tools import BaseTool


class DestinationSearchTool(BaseTool):
    name: str = "destination_search"
    description: str = "Find mock attractions and local experiences for a destination."
    def _run(self, destination: str) -> str:
        return f"Mock search results for {destination}: historic centre walking tour, local food market, museum district, public park, and a guided cultural experience. Source: local prototype catalogue."


class WeatherTool(BaseTool):
    name: str = "weather_forecast"
    description: str = "Return a mock weather forecast for destination and dates."
    def _run(self, destination: str, dates: str) -> str:
        return f"Mock weather for {destination} during {dates}: mild conditions expected. Check an official weather service near departure. Source: mock weather tool."


class HotelTransportTool(BaseTool):
    name: str = "hotel_transport_search"
    description: str = "Return mock hotel and transport options and estimates."
    def _run(self, destination: str, starting_location: str, duration_days: int) -> str:
        hotel = 3500 * duration_days
        transport = 9000
        return f"Mock options: Central Stay Hotel at ₹3,500/night (₹{hotel:,} total); return economy transport from {starting_location} at ₹{transport:,}; local transit pass ₹1,200. Sources: mock hotel and transport tools."


class BudgetCalculatorTool(BaseTool):
    name: str = "budget_calculator"
    description: str = "Calculate estimated trip cost from budget inputs."
    def _run(self, total_budget: float, duration_days: int) -> str:
        hotel = 3500 * duration_days
        transport = 9000
        food = 1200 * duration_days
        activities = 1000 * duration_days
        total = hotel + transport + food + activities + 1200
        difference = total_budget - total
        status = "within budget" if difference >= 0 else "over budget"
        return f"Estimated total ₹{total:,.0f}: hotel ₹{hotel:,.0f}, transport ₹{transport:,}, local transit ₹1,200, food ₹{food:,.0f}, activities ₹{activities:,.0f}. Budget ₹{total_budget:,.0f}; {status} by ₹{abs(difference):,.0f}."


class RoutingTool(BaseTool):
    name: str = "routing_schedule"
    description: str = "Create mock day-by-day routing guidance."
    def _run(self, destination: str, duration_days: int, interests: str) -> str:
        days = []
        for day in range(1, duration_days + 1):
            focus = interests if day == 1 else "nearby attractions and local dining"
            days.append(f"Day {day}: explore {destination} using walkable/short-transit stops focused on {focus}.")
        return " ".join(days) + " Source: mock routing tool."

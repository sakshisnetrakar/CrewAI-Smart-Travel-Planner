"""Deterministic local plan when CrewAI/Ollama is unavailable."""

def make_fallback_plan(data: dict) -> str:
    days = int(data["duration_days"])
    hotel = 3500 * days
    transport, transit, food, activities = 9000, 1200, 1200 * days, 1000 * days
    total = hotel + transport + transit + food + activities
    difference = data["budget"] - total
    itinerary = "\n".join(f"Day {day}: Explore {data['destination']} with {data['interests']}; use walkable stops or short local-transit journeys." for day in range(1, days + 1))
    alternative = "" if difference >= 0 else "\nAlternative: choose a ₹2,500/night stay, use public transit, or shorten paid activities to meet the budget."
    return f"""LOCAL MOCK TRAVEL PLAN
Destination: {data['destination']} | Dates: {data['travel_dates']} | From: {data['starting_location']}

Recommended attractions: historic centre walking tour, local food market, museum district, public park, and guided cultural experience.
Hotel and transport: Central Stay Hotel (mock) ₹3,500/night; return economy transport (mock) ₹9,000; local transit pass ₹1,200.

Day-by-day itinerary:
{itinerary}

Estimated expenses: Hotel ₹{hotel:,}; transport ₹{transport:,}; local transit ₹{transit:,}; food ₹{food:,}; activities ₹{activities:,}. Total ₹{total:,}.
Budget comparison: Budget ₹{data['budget']:,.0f}; {'within budget by' if difference >= 0 else 'over budget by'} ₹{abs(difference):,.0f}.{alternative}

Sources: local prototype catalogue, mock weather tool, mock hotel/transport tool, mock routing tool. Verify all prices, availability, weather, and travel requirements before booking."""

# CrewAI Smart Travel Planner

A local-only multi-agent travel-planning prototype using CrewAI. It defines five agents: coordinator, destination researcher, hotel/transport researcher, budget analyst, and itinerary planner. Tasks run sequentially and later tasks receive earlier outputs as context.

## Local setup

```cmd
cd "C:\Users\Sakshi S Netrakar\Desktop\CrewAI Smart Travel Planner"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## CrewAI + Ollama mode

Install Ollama, then run:

```cmd
ollama pull llama3.2
ollama serve
```

Copy `.env.example` to `.env` if you need different Ollama settings. With CrewAI and Ollama available, the app runs the five-agent sequential workflow. Otherwise, it provides a fully local mock fallback so the interface remains usable.

## External services

The search, weather, hotel, transport, and routing tools currently return labelled mock data. This keeps the project local and credential-free. Replace their implementations in `travel_tools.py` only with authorised APIs and credentials stored outside source control.

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from fallback_planner import make_fallback_plan

app = FastAPI(title="CrewAI Smart Travel Planner")
PAGE = Path(__file__).parent / "static" / "index.html"


class TravelRequest(BaseModel):
    destination: str = Field(min_length=2, examples=["Jaipur"])
    starting_location: str = Field(min_length=2, examples=["Bengaluru"])
    travel_dates: str = Field(min_length=3, examples=["15-18 November 2026"])
    duration_days: int = Field(ge=1, le=14, examples=[3])
    budget: float = Field(gt=0, examples=[50000])
    interests: str = Field(min_length=2, examples=["sightseeing, food, shopping"])


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(PAGE)


@app.post("/plan")
def plan(request: TravelRequest):
    data = request.model_dump()
    try:
        from crewai_workflow import run_crewai_plan
        return {"plan": run_crewai_plan(data), "engine": "CrewAI with local Ollama", "sources_are_mock": True}
    except Exception as error:
        return {"plan": make_fallback_plan(data), "engine": "local mock fallback", "sources_are_mock": True, "note": f"CrewAI/Ollama was unavailable: {type(error).__name__}"}


@app.get("/health")
def health():
    return {"status": "ok", "deployment": "local prototype only"}

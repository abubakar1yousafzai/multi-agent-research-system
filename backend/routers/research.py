from fastapi import APIRouter, HTTPException
from models.research import FinalReport, ResearchRequest
from agents.orchestrator import Orchestrator

router = APIRouter(prefix="/api/v1/research", tags=["research"])


@router.post("", response_model=FinalReport)
async def run_research(request: ResearchRequest):
    orchestrator = Orchestrator(
        user_query=request.user_query,
        session_id=request.session_id,
    )
    report = await orchestrator.run()
    return report

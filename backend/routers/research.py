import asyncio

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.research import FinalReport, ResearchRequest
from agents.orchestrator import Orchestrator

router = APIRouter(prefix="/api/v1/research", tags=["research"])

_active_orchestrators: dict[str, Orchestrator] = {}


@router.post("", response_model=FinalReport)
async def run_research(request: ResearchRequest):
    orchestrator = _active_orchestrators.get(request.session_id)
    if orchestrator is None:
        orchestrator = Orchestrator(
            user_query=request.user_query,
            session_id=request.session_id,
        )
        _active_orchestrators[request.session_id] = orchestrator
    report = await orchestrator.run()
    return report


@router.get("/stream/{session_id}")
async def stream_status(session_id: str):
    orchestrator = _active_orchestrators.get(session_id)
    if orchestrator is None:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        try:
            while True:
                try:
                    update = await asyncio.wait_for(
                        orchestrator.status_queue.get(), timeout=1.0
                    )
                    yield f"data: {update.model_dump_json()}\n\n"
                    if update.agent == "reporter" and update.status == "completed":
                        break
                except asyncio.TimeoutError:
                    if orchestrator._run_complete.is_set() and orchestrator.status_queue.empty():
                        break
        finally:
            _active_orchestrators.pop(session_id, None)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

import asyncio
import os
import logging
from typing import Optional

from openai import OpenAI
from models.research import AgentResult, FinalReport, StatusUpdate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

groq_client: Optional[OpenAI] = None


def get_groq_client() -> OpenAI:
    global groq_client
    if groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        groq_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )
    return groq_client


async def mock_web_search(input_data: dict) -> AgentResult:
    logger.info("mock_web_search called with input: %s", input_data)
    return AgentResult(
        agent_name="web_search",
        status="completed",
        data={"results": ["result1", "result2"]},
    )


async def mock_research(input_data: dict) -> AgentResult:
    logger.info("mock_research called with input: %s", input_data)
    return AgentResult(
        agent_name="research",
        status="completed",
        data={"findings": ["finding1", "finding2"]},
    )


async def mock_analyzer(input_data: dict) -> AgentResult:
    logger.info("mock_analyzer called with input: %s", input_data)
    return AgentResult(
        agent_name="analyzer",
        status="completed",
        data={"analysis": "analyzed results"},
    )


async def mock_reporter(input_data: dict) -> AgentResult:
    logger.info("mock_reporter called with input: %s", input_data)
    return AgentResult(
        agent_name="reporter",
        status="completed",
        data={"report": "final structured report"},
    )


class Orchestrator:
    def __init__(self, user_query: str, session_id: str):
        self.user_query = user_query
        self.session_id = session_id
        self.agent_statuses: list[AgentResult] = []
        self._status_callbacks: list[callable] = []
        self.status_queue: asyncio.Queue[StatusUpdate] = asyncio.Queue()
        self._run_complete: asyncio.Event = asyncio.Event()

    def on_status_update(self, callback: callable):
        self._status_callbacks.append(callback)

    def _emit_status(self, agent: str, status: str, detail: Optional[str] = None):
        update = StatusUpdate(agent=agent, status=status, detail=detail)
        for cb in self._status_callbacks:
            cb(update)
        self.status_queue.put_nowait(update)

    async def _run_agent(self, name: str, func: callable, input_data: dict) -> AgentResult:
        logger.info("Agent '%s' starting", name, extra={"agent": name, "phase": "start"})
        self._emit_status(name, "running")
        try:
            result = await func(input_data)
            result.agent_name = name
            self.agent_statuses.append(result)
            logger.info(
                "Agent '%s' completed", name,
                extra={"agent": name, "phase": "completed", "status": result.status},
            )
            self._emit_status(name, "completed")
            return result
        except Exception as e:
            detail = str(e)
            logger.error(
                "Agent '%s' failed: %s", name, detail,
                extra={"agent": name, "phase": "failed", "error": detail},
            )
            error_result = AgentResult(agent_name=name, status="error", data={}, error=detail)
            self.agent_statuses.append(error_result)
            self._emit_status(name, "error", detail=detail)
            return error_result

    async def run(self) -> FinalReport:
        logger.info(
            "Orchestrator starting pipeline for query: %s, session: %s",
            self.user_query,
            self.session_id,
            extra={"phase": "pipeline_start", "query": self.user_query, "session": self.session_id},
        )

        web_result = await self._run_agent("web_search", mock_web_search, {"query": self.user_query})
        research_result = await self._run_agent("research", mock_research, web_result.data if web_result.status != "error" else {})
        analyzer_result = await self._run_agent("analyzer", mock_analyzer, research_result.data if research_result.status != "error" else {})
        reporter_result = await self._run_agent("reporter", mock_reporter, analyzer_result.data if analyzer_result.status != "error" else {})

        last_result = reporter_result if reporter_result.status != "error" else \
                      analyzer_result if analyzer_result.status != "error" else \
                      research_result if research_result.status != "error" else \
                      web_result

        report = FinalReport(
            session_id=self.session_id,
            summary=last_result.data.get("report", "Partial results with some agent failures") if last_result.status != "error" else "Pipeline completed with errors",
            details={
                "query": self.user_query,
                "agent_count": len(self.agent_statuses),
            },
            agent_statuses=self.agent_statuses,
        )
        logger.info(
            "Orchestrator pipeline complete for session: %s", self.session_id,
            extra={"phase": "pipeline_end", "session": self.session_id, "status": "completed"},
        )
        self._run_complete.set()
        return report

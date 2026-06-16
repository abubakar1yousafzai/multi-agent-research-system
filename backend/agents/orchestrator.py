import asyncio
import os
import logging
from typing import Optional

from openai import OpenAI
from models.research import AgentResult, FinalReport, StatusUpdate

logging.basicConfig(level=logging.INFO)
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

    async def run(self) -> FinalReport:
        logger.info(
            "Orchestrator starting pipeline for query: %s, session: %s",
            self.user_query,
            self.session_id,
        )

        self._emit_status("web_search", "running")
        web_result = await mock_web_search({"query": self.user_query})
        self.agent_statuses.append(web_result)
        self._emit_status("web_search", "completed")

        self._emit_status("research", "running")
        research_result = await mock_research(web_result.data)
        self.agent_statuses.append(research_result)
        self._emit_status("research", "completed")

        self._emit_status("analyzer", "running")
        analyzer_result = await mock_analyzer(research_result.data)
        self.agent_statuses.append(analyzer_result)
        self._emit_status("analyzer", "completed")

        self._emit_status("reporter", "running")
        reporter_result = await mock_reporter(analyzer_result.data)
        self.agent_statuses.append(reporter_result)
        self._emit_status("reporter", "completed")

        report = FinalReport(
            session_id=self.session_id,
            summary=reporter_result.data.get("report", "No summary generated"),
            details={
                "query": self.user_query,
                "agent_count": len(self.agent_statuses),
            },
            agent_statuses=self.agent_statuses,
        )
        logger.info("Orchestrator pipeline complete for session: %s", self.session_id)
        self._run_complete.set()
        return report

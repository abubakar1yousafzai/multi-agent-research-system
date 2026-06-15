from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.research import router as research_router

app = FastAPI(title="Multi-Agent Research System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)

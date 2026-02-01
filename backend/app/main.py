from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.api import notes, search, chat, graph, study

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal Knowledge System API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["graph"])
app.include_router(study.router, prefix="/api/v1/study", tags=["study"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

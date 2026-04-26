"""
Sophie Chatbot API - Main Entry Point
File main.py đã được tách nhỏ thành các module trong thư mục backend/
"""
from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path
import sys

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Import từ backend modules
from backend.database import init_database
from backend.routes import auth_routes, conversation_routes, admin_routes, admin_batch_routes
from backend.routes import product_routes
# Initialize FastAPI app
app = FastAPI(
    title="Sophie Chatbot API",
    description="API for Sophie - AI Shopping Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
def _log_runtime_diagnostics() -> None:
    project_root = Path(__file__).resolve().parents[1]
    expected_venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    current_python = Path(sys.executable).resolve()

    logger.info("Runtime python=%s", current_python)
    if expected_venv_python.exists() and current_python != expected_venv_python.resolve():
        logger.warning(
            "Backend is not running with workspace venv. expected=%s current=%s",
            expected_venv_python,
            current_python,
        )

    try:
        import pydantic

        version = getattr(pydantic, "__version__", "unknown")
        logger.info("Runtime pydantic=%s", version)
        if not str(version).startswith("2."):
            logger.warning(
                "Detected pydantic %s. LangChain in this project requires pydantic 2.x.",
                version,
            )
    except Exception:
        logger.exception("Unable to inspect pydantic runtime version")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    _log_runtime_diagnostics()
    init_database()
    logger.info("FastAPI application started")

# Register routers
app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(conversation_routes.router, tags=["Conversations"])
app.include_router(admin_routes.router, tags=["Admin"])
app.include_router(admin_batch_routes.router, tags=["Admin Batch"])
app.include_router(product_routes.router, tags=["Products"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sophie Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Compatibility search endpoint used by the frontend (/search?q=...)
@app.get("/search")
async def search_products(q: Optional[str] = None, limit: int = 50, offset: int = 0):
    """Simple proxy endpoint that returns products from the DB.

    This calls into the products router handler so frontend code that
    requests `/search?q=...` keeps working.
    """
    return await product_routes.list_products(q=q, limit=limit, offset=offset)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8010, reload=True)

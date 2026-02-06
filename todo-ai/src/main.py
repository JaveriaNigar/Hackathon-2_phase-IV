from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat as chat_router
from src.api.routes import auth as auth_router
from src.api.routes import user as user_router
from src.api.routes import tasks as tasks_router
from src.database.session import engine
from src.models import *
from sqlmodel import SQLModel
from src.utils.logging import setup_logger

# Configure logging
logger = setup_logger()

# Create FastAPI app instance
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for the AI-powered Todo Chatbot application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://huggingface.co",
        "https://*.huggingface.co"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    from src.utils.logging import log_api_call
    
    # Skip logging for OPTIONS requests to avoid interference with CORS
    if request.method == "OPTIONS":
        return await call_next(request)

    start_time = time.time()
    logger.info(f"[REQ] {request.method} {request.url.path}")
    
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(f"[RES] Status: {response.status_code}, Process Time: {process_time:.2f}ms\n")

    # Log the API call with timing
    log_api_call(
        logger=logger,
        endpoint=request.url.path,
        method=request.method,
        ip_address=request.client.host if request.client else None,
        response_time=process_time
    )

    return response

# Create database tables
@app.on_event("startup")
def on_startup():
    # Ensure all models are registered with SQLModel metadata
    # from src.models import User, Task # Already imported via *
    SQLModel.metadata.create_all(engine)

# Include API routes
app.include_router(chat_router.router, prefix="/api/{user_id}", tags=["chat"])
app.include_router(auth_router.router, prefix="/api", tags=["auth"])
app.include_router(user_router.router, prefix="/api", tags=["user"])
app.include_router(tasks_router.router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

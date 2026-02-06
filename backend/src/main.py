from fastapi import FastAPI, Request
import os
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat
from src.api.routes import auth
from src.api.routes import user
from src.api.routes import tasks
from src.database.session import engine
from src.models import *  # Import all models to register them with SQLModel
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
# In production, specify the origins that are allowed to make requests
# For development, you can use a wildcard "*"
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],  # Allow all headers but restrict methods
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    from src.utils.logging import log_api_call
    import time

    start_time = time.time()

    logger.info(f"[REQ] {request.method} {request.url.path}")
    if "Authorization" in request.headers:
        logger.info(f"[REQ] Auth Header: {request.headers['Authorization'][:20]}...")
    else:
        logger.info("[REQ] NO Auth Header")

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
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
    from src.models import User, Task
    SQLModel.metadata.create_all(engine)

# Include API routes
app.include_router(chat.router, prefix="/api/{user_id}", tags=["chat"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


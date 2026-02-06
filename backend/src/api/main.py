from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes.chat import router as chat_router
from .routes.auth import router as auth_router
from .routes.tasks import router as tasks_router
from .routes.user import router as user_router
from ..config.database import engine
from ..models.task import Task, Conversation, Message
from sqlmodel import SQLModel

# Create the FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for the AI-powered Todo Chatbot application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(chat_router, prefix="/api/{user_id}", tags=["chat"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)
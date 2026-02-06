from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlmodel>=0.0.16",
        "psycopg2-binary>=2.9.9",
        "python-jose[cryptography]>=3.3.0",
        "better-auth>=0.0.1-rc.1",
        "pydantic>=2.9.2",
        "python-dotenv>=1.0.1",
        "openai>=1.51.2",
        "google-generativeai>=0.8.3",
        "asyncpg>=0.30.0",
        "alembic>=1.13.3",
        "pydantic-settings>=2.6.1",
        "bcrypt>=3.2.0",
        "passlib[bcrypt]>=1.7.4",
    ],
    python_requires=">=3.9",
)
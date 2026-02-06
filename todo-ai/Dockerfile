FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install the package in development mode to make src accessible
RUN pip install -e .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]
FROM python:3.11-slim

WORKDIR /app

# Install git and other system dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app

# Expose port
EXPOSE 8000

# Run commands
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

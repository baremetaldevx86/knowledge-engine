FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for pgvector/psycopg2 if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Hugging Face Spaces defaults to 7860)
EXPOSE 7860

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

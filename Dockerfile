FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script files
COPY scripts/ ./scripts

# Default command to run the cleaner script
CMD ["python", "./scripts/cleaner.py"]

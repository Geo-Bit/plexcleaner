FROM python:3.11-slim

# Install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script files
COPY scripts/ ./scripts

# Create the cron job
RUN echo "0 3 * * * /usr/local/bin/python /app/scripts/cleaner.py >> /var/log/cron.log 2>&1" > /etc/cron.d/cleaner-cron
RUN chmod 0644 /etc/cron.d/cleaner-cron
RUN crontab /etc/cron.d/cleaner-cron

# Create the log file
RUN touch /var/log/cron.log

# Start cron in the foreground
CMD ["cron", "-f"]

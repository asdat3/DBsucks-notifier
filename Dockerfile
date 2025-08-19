FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cron job file
COPY cron_job.sh /etc/cron.d/db_notifier
RUN chmod +x /etc/cron.d/db_notifier
RUN chmod +x /app/cron_job.sh

# Create log directory
RUN mkdir -p /var/log/cron

# Apply cron job
RUN crontab /etc/cron.d/db_notifier

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

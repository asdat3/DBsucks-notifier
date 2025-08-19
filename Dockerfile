FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cron job file in the correct format
RUN echo "0 5 * * * cd /app && python3 -c \"import os; os.environ['RUN_TIME'] = 'morning'; exec(open('main.py').read())\" >> /var/log/cron/db_notifier.log 2>&1" > /etc/cron.d/db_notifier
RUN echo "0 22 * * * cd /app && python3 -c \"import os; os.environ['RUN_TIME'] = 'evening'; exec(open('main.py').read())\" >> /var/log/cron/db_notifier.log 2>&1" >> /etc/cron.d/db_notifier

# Create log directory
RUN mkdir -p /var/log/cron

# Apply cron job
RUN crontab /etc/cron.d/db_notifier

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

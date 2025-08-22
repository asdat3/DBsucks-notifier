# DB Sucks Notifier

A Deutsche Bahn train connection notifier that runs twice daily to check for connections to/from specific stations.

## Docker Setup

This application is containerized and runs automatically twice daily:
- **5:00 AM**: Checks connections for today
- **10:00 PM**: Checks connections for tomorrow

### Prerequisites

- Docker and Docker Compose installed
- Environment variables configured

### Environment Variables

Create a `.env` file with the following variables:

```env
DB_CLIENT_ID=your_db_client_id
DB_CLIENT_SECRET=your_db_client_secret
HOURS_TO_CHECK='[5,21]'
UTC_CORRECTION=-2
DISCORD_WEBHOOK_URL=your_discord_webhook_url
STATION_CONFIGS={"station_name": "Berlin Hbf", "target_hours": [6, 7, 8], "dest_station_keywords": ["BER"], "transport_type_trains": ["ICE", "IC"]}
```

### Running with Docker Compose

1. **Build and start the service:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f db-notifier
   ```

3. **Stop the service:**
   ```bash
   docker-compose down
   ```

4. **Rebuild after code changes:**
   ```bash
   docker-compose up -d --build
   ```

### Manual Testing

To test the application manually:

```bash
# Test morning logic (today's date)
docker exec db-notifier python3 -c "
import os
os.environ['RUN_TIME'] = 'morning'
exec(open('/app/main.py').read())
"

# Test evening logic (tomorrow's date)
docker exec db-notifier python3 -c "
import os
os.environ['RUN_TIME'] = 'evening'
exec(open('/app/main.py').read())
"
```

### Logs

Application logs are stored in the `./logs` directory and can be viewed with:
```bash
tail -f logs/db_notifier.log
```

## Development

For local development without Docker, use the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
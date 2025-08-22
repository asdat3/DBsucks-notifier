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

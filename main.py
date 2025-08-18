from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
import requests
from config import settings

# Initialize authentication with settings
auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)
stations = StationHelper().find_stations_by_name(settings.station_name)
station = stations[0]
tth = TimetableHelper(StationHelper(), auth)

def send_discord_alert(message: str):
    """Send a Discord alert via webhook"""
    payload = {
        "content": message,
        "username": "DB Sucks Notifier"
    }
    
    try:
        response = requests.post(settings.discord_webhook_url, json=payload)
        response.raise_for_status()
        print(f"Discord alert sent successfully: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord alert: {e}")

trains = tth.get_timetable()
changes = tth.get_timetable_changes(trains)

if not trains or all(tr.status == "cancelled" for tr in trains):
    alert_message = f"🚨 **DB Sucks Alert** 🚨\nAll trains at {settings.station_name} are cancelled or unavailable!"
    send_discord_alert(alert_message)

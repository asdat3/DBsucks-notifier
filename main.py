from datetime import datetime, timedelta
from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
from db_timetable_api import timetable
from config import settings
from modules.analyzers import analyze_to_from_connections
from modules.notifier.discord import send_discord_message
import json
import os

db = timetable.timetable_api(clientid=settings.db_client_id, clientsecret=settings.db_client_secret)
auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)

# Determine timing based on RUN_TIME environment variable
run_time = os.getenv('RUN_TIME', 'evening')  # Default to evening if not specified

if run_time == 'morning':
    # Morning run at 5 AM - tomorrow variable should be today
    tomorrow = datetime.now().strftime("%Y-%m-%d")
    print(f"Running morning check for {tomorrow}")
else:
    # Evening run at 10 PM - tomorrow variable should be tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Running evening check for {tomorrow}")

for config in settings.config_list:
    station = StationHelper().find_stations_by_name(config["station_name"])[0] # Todo: add a try except (if no station found)
    print(f"Station: {station.NAME} ({station.EVA_NR})")

    for TARGET_HOUR in config["target_hours"]:
        plan = db.get_timetable(str(station.EVA_NR), tomorrow, TARGET_HOUR)
        # print(json.dumps(plan, indent=4))

        # Analyze the train data for BER Airport connections
        if plan:
            analysis = analyze_to_from_connections(plan,TARGET_HOUR,dest_station_keywords=config["dest_station_keywords"],transport_type_trains=config["transport_type_trains"])
            send_discord_message(analysis)
        else:
            print("No timetable data received from API.")

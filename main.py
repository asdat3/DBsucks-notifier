from datetime import datetime, timedelta
from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
from db_timetable_api import timetable
from config import settings
from modules.analyzers import analyze_to_from_connections
from modules.notifier.discord import send_discord_message

TARGET_HOUR = "06"
# tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
tomorrow = (datetime.now()).strftime("%Y-%m-%d") # for testing lets use today as data isnt available yet for tomorrow

db = timetable.timetable_api(clientid=settings.db_client_id, clientsecret=settings.db_client_secret)
auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)
station = StationHelper().find_stations_by_name(settings.station_name)[0] # Todo: add a try except (if no station found)
print(f"Station: {station.NAME} ({station.EVA_NR})")

plan = db.get_timetable(str(station.EVA_NR), tomorrow, TARGET_HOUR)

# Analyze the train data for BER Airport connections
if plan:
    analysis = analyze_to_from_connections(plan,TARGET_HOUR,dest_station_keywords=["BER","Flughafen"],transport_type_trains=["RB","RE"])
    send_discord_message(analysis)
else:
    print("No timetable data received from API.")

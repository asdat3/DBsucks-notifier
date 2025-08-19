from datetime import datetime, timedelta
from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
from db_timetable_api import timetable
from config import settings
from modules.analyzers import analyze_to_from_connections
import json

CLIENT_ID = settings.db_client_id
CLIENT_SECRET = settings.db_client_secret
TARGET_HOUR = "06"

# tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
tomorrow = (datetime.now()).strftime("%Y-%m-%d") # for testing lets use today as data isnt available yet for tomorrow

db = timetable.timetable_api(clientid=CLIENT_ID, clientsecret=CLIENT_SECRET)
auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)
station = StationHelper().find_stations_by_name(settings.station_name)[0] # Todo: add a try except (if no station found)
print(f"Station: {station.NAME} ({station.EVA_NR})")

plan = db.get_timetable(str(station.EVA_NR), tomorrow, "06")

# Analyze the train data for BER Airport connections
if plan:
    analysis = analyze_to_from_connections(plan,dest_station_keywords=["BER","Flughafen"],transport_type_trains=["RB","RE"])
    print(json.dumps(analysis, indent=4))
else:
    print("No timetable data received from API.")

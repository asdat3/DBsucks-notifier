from datetime import datetime, timedelta
from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
from db_timetable_api import timetable
from config import settings

CLIENT_ID = settings.db_client_id
CLIENT_SECRET = settings.db_client_secret
TARGET_HOUR = "06"
TARGET_MINUTE = "26"

db = timetable.timetable_api(clientid=CLIENT_ID, clientsecret=CLIENT_SECRET)
auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)
stations = StationHelper().find_stations_by_name(settings.station_name)
station = stations[0]
print(f"Station: {station.NAME} ({station.EVA_NR})")
EVA = station.EVA_NR


tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

try:
    plan = db.get_timetable(EVA, tomorrow)
except Exception as e:
    print(f"Plan-Daten nicht verfügbar ({e}).")
    plan = {"timetable": []}

try:
    changes = db.get_changes(EVA)
except Exception as e:
    print(f"Änderungen nicht verfügbar ({e}).")
    changes = {"timetable": []}


from datetime import datetime, timedelta
from deutsche_bahn_api import ApiAuthentication, StationHelper, TimetableHelper
from db_timetable_api import timetable
from app.config import settings
from app.modules.analyzers import analyze_to_from_connections
from app.modules.notifier.discord import send_discord_message

def main():
    db = timetable.timetable_api(clientid=settings.db_client_id, clientsecret=settings.db_client_secret)
    auth = ApiAuthentication(settings.db_client_id, settings.db_client_secret)

    if datetime.now().hour < 18:
        tomorrow = datetime.now().strftime("%Y-%m-%d")
        print(f"Running morning check for {tomorrow} (today)")
    else:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"Running evening check for {tomorrow} (tomorrow)")

    for config in settings.config_list:
        station = StationHelper().find_stations_by_name(config["station_name"])[0] # Todo: add a try except (if no station found)
        print(f"Station: {station.NAME} ({station.EVA_NR})")

        # Collect analysis for all target hours
        all_hours_analysis = []
        for TARGET_HOUR in config["target_hours"]:
            plan = db.get_timetable(str(station.EVA_NR), tomorrow, TARGET_HOUR)
            # print(json.dumps(plan, indent=4))

            if plan:
                analysis = analyze_to_from_connections(plan, TARGET_HOUR, dest_station_keywords=config["dest_station_keywords"], transport_type_trains=config["transport_type_trains"])
                all_hours_analysis.append(analysis)
            else:
                print(f"No timetable data received from API for hour {TARGET_HOUR}.")
        
        # Send one message per station with all hours analysis
        if all_hours_analysis:
            send_discord_message(all_hours_analysis, tomorrow, station.NAME)
        else:
            print(f"No timetable data available for station {station.NAME}")

if __name__ == "__main__":
    main()

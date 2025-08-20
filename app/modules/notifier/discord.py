import requests
from app.config import settings
from datetime import datetime

def send_discord_message(analysis,tomorrow):
    """
    Send a message to a Discord webhook.
    Args:
        analysis: Analysis results with details about dest_station_keywords connections
        tomorrow: date when the check is running
    """
    message = {}
    message["embeds"] = []

    description_list_all_connections = f"All connections: ({tomorrow})\n"
    for connection in analysis["all_connections"]:
        if connection['line'] == "":
            description_list_all_connections += f"**{connection['transport_type']}** {analysis['target_hour']}:{connection['time']} - {connection['direction'].lower()} {analysis['destination_station']}\n"
        else:
            if str(connection['line']).isdigit():
                connection['line'] = connection['transport_type'] + connection['line']
            description_list_all_connections += f"**{connection['line']}** ({connection['transport_type']}) {analysis['target_hour']}:{connection['time']} - {connection['direction'].lower()} {analysis['destination_station']}\n"


    if analysis["trains_to"] < 1:
        message_embed = {
            "title": f"Train to {analysis['destination_station']} is **NOT** running ({analysis['station']})",
            "description": description_list_all_connections,
            "color": 16711680,
            "footer": {
                "text": "DBSucksUpdater"
            },
            "timestamp": datetime.now().isoformat()
        }
    else:
        message_embed = {
            "title": f"Train to {analysis['destination_station']} is running ({analysis['station']})",
            "description": description_list_all_connections,
            "color": 4718336,
            "footer": {
                "text": "DBSucksUpdater"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    message["embeds"].append(message_embed)

    response = requests.post(settings.discord_webhook_url, json=message)
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code} {response.text}")
    else:
        print("Message sent to Discord successfully")
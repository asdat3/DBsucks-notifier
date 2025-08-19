import requests
from config import settings
from datetime import datetime

def send_discord_message(analysis):
    """
    Send a message to a Discord webhook.
    Args:
        analysis: Analysis results with details about dest_station_keywords connections
    """
    message = {}
    message["embeds"] = []

    if analysis["trains_to"] < 1:
        description_list_all_connections = "All connections:\n"
        for connection in analysis["all_connections"]:
            description_list_all_connections += f"**{connection['line']}** ({connection['transport_type']}) {analysis['target_hour']}:{connection['time']} - {connection['direction'].lower()} {analysis['destination_station']}\n"

        message_embed = {
            "title": f"Train to {analysis['destination_station']} is **NOT** running",
            "description": description_list_all_connections,
            "color": 16711680,
            "footer": {
                "text": "DBSucksUpdater"
            },
            "timestamp": datetime.now().isoformat()
        }
    else:
        description_list_all_connections = "All connections:\n"
        for connection in analysis["all_connections"]:
            description_list_all_connections += f"**{connection['line']}** ({connection['transport_type']}) {analysis['target_hour']}:{connection['time']} - {connection['direction'].lower()} {analysis['destination_station']}\n"
        message_embed = {
            "title": f"Train to {analysis['destination_station']} is running",
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
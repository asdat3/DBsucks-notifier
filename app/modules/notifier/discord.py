import requests
from app.config import settings
from datetime import datetime

def send_discord_message(all_hours_analysis, tomorrow, station_name):
    """
    Send a message to a Discord webhook with analysis for all hours.
    Args:
        all_hours_analysis: List of analysis results for all target hours
        tomorrow: date when the check is running
        station_name: name of the station being analyzed
    """
    message = {}
    message["embeds"] = []

    # Calculate overall status across all hours
    total_trains_to = sum(analysis["trains_to"] for analysis in all_hours_analysis)
    total_buses_to = sum(analysis["buses_to"] for analysis in all_hours_analysis)
    total_connections = sum(analysis["total_connections"] for analysis in all_hours_analysis)
    
    # Determine overall status - train is running if there's at least one train in any hour
    overall_train_running = total_trains_to > 0
    overall_replaced_by_bus = total_buses_to > 0 and total_trains_to == 0

    # Create description showing all hours
    description = f"**📍 Station:** {station_name}\n**📅 Date:** {tomorrow}\n\n"
    
    for analysis in all_hours_analysis:
        hour = analysis["target_hour"]
        trains_to = analysis["trains_to"]
        buses_to = analysis["buses_to"]
        
        if trains_to > 0:
            status = f"🚆 **{hour}:00** - {trains_to} train(s) running"
        elif buses_to > 0:
            status = f"🚌 **{hour}:00** - {buses_to} bus(es) replacing trains"
        else:
            status = f"❌ **{hour}:00** - No connections"
        
        description += f"{status}\n"
    
    # Create fancy detailed breakdown of all connections
    description += "\n🚂 **ALL CONNECTIONS** 🚂\n"
    
    for analysis in all_hours_analysis:
        hour = analysis["target_hour"]
        if analysis["all_connections"]:
            # Group connections by direction and transport type
            to_connections = [conn for conn in analysis["all_connections"] if conn['direction'] == 'TO']
            from_connections = [conn for conn in analysis["all_connections"] if conn['direction'] == 'FROM']
            
            description += f"\n🕐 **{hour}:00** "
            
            # TO connections (going to destination)
            if to_connections:
                description += f"- **TO {analysis['destination_station']}:**\n"
                for conn in to_connections:
                    transport_emoji = "🚌" if conn['is_bus'] else "🚆"
                    direction_emoji = "➡️"
                    
                    # Format line number nicely
                    line_display = conn['line'] if conn['line'] else "N/A"
                    if str(line_display).isdigit():
                        line_display = f"{conn['transport_type']}{line_display}"
                    
                    # Format platform
                    platform_display = f"Pl.{conn['platform']}" if conn['platform'] else ""
                    
                    description += f"  {transport_emoji} {direction_emoji} **{line_display}** | {hour}:{conn['time'].replace(":", "")} | {platform_display}\n"
            
            # FROM connections (coming from destination)
            if from_connections:
                description += f"> 🔄 **FROM {analysis['destination_station']}:**\n"
                for conn in from_connections:
                    transport_emoji = "> 🚌" if conn['is_bus'] else "> 🚆"
                    direction_emoji = "⬅️"
                    
                    # Format line number nicely
                    line_display = conn['line'] if conn['line'] else "N/A"
                    if str(line_display).isdigit():
                        line_display = f"{conn['transport_type']}{line_display}"
                    
                    # Format platform
                    platform_display = f"Pl.{conn['platform']}" if conn['platform'] else ""
                    
                    description += f"  {transport_emoji} {direction_emoji} **{line_display}** | {hour}:{conn['time'].replace(":", "")} | {platform_display}\n"
            
            if not to_connections and not from_connections:
                description += "  ❌ No connections found\n"

    # Set color based on overall status
    if overall_train_running:
        color = 4718336  # Green
        title = f"✅ Trains to {all_hours_analysis[0]['destination_station']} ARE running ({station_name})"
    else:
        color = 16711680  # Red
        title = f"❌ Trains to {all_hours_analysis[0]['destination_station']} are NOT running ({station_name})"

    message_embed = {
        "title": title,
        "description": description,
        "color": color,
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
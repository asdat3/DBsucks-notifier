
def analyze_to_from_connections(train_data,dest_station_keywords=["BER","Flughafen"],transport_type_trains=["RB","RE","ICE","IC"]):
    """
    Analyze train data to determine if trains to dest_station_keywords are running or replaced by buses.
    
    Args:
        train_data: Dictionary containing station and trains information
        dest_station_keywords: List of keywords to check for in the departure/arrival path
        transport_type_trains: List of transport types to check for in the departure/arrival path
        
    Returns:
        dict: Analysis results with details about dest_station_keywords connections
    """
    ber_connections = []
    
    for train in train_data.get('trains', []):
        # Check if this train/bus goes to BER Airport
        is_to_ber = False
        is_from_ber = False
        
        # Check departure path (dp) for trains going TO BER
        if 'dp' in train:
            path = train['dp'].get('ppth', '')
            if any(keyword.lower() in path.lower() for keyword in dest_station_keywords):
                is_to_ber = True
        
        # Check arrival path (ar) for trains coming FROM BER
        if 'ar' in train:
            path = train['ar'].get('ppth', '')
            if any(keyword.lower() in path.lower() for keyword in dest_station_keywords):
                is_from_ber = True
        
        if is_to_ber or is_from_ber:
            # Determine if it's a train or bus
            transport_type = train.get('tl', {}).get('c', 'Unknown')
            is_bus = transport_type == 'Bus'
            is_train = transport_type in transport_type_trains
            
            # Get timing information
            if 'dp' in train:
                departure_time = train['dp'].get('pt', '')
                platform = train['dp'].get('pp', '')
                line = train['dp'].get('l', '')
            else:
                departure_time = train['ar'].get('pt', '')
                platform = train['ar'].get('pp', '')
                line = train['ar'].get('l', '')
            
            # Convert timestamp to readable time
            if departure_time:
                try:
                    # Assuming timestamp format like "2508190635" (DDMMYYYYHHMM)
                    day = departure_time[:2]
                    month = departure_time[2:4]
                    year = departure_time[4:8]
                    hour = departure_time[8:10]
                    minute = departure_time[10:12]
                    readable_time = f"{hour}:{minute}"
                except:
                    readable_time = departure_time
            else:
                readable_time = "Unknown"
            
            connection_info = {
                'id': train.get('id', ''),
                'transport_type': transport_type,
                'is_bus': is_bus,
                'is_train': is_train,
                'line': line,
                'time': readable_time,
                'platform': platform,
                'direction': 'TO' if is_to_ber else 'FROM',
                'path': train.get('dp', {}).get('ppth', '') or train.get('ar', {}).get('ppth', '')
            }
            
            ber_connections.append(connection_info)
    
    # Analyze the results
    buses_to_ber = [conn for conn in ber_connections if conn['is_bus'] and conn['direction'] == 'TO']
    trains_to_ber = [conn for conn in ber_connections if conn['is_train'] and conn['direction'] == 'TO']
    buses_from_ber = [conn for conn in ber_connections if conn['is_bus'] and conn['direction'] == 'FROM']
    trains_from_ber = [conn for conn in ber_connections if conn['is_train'] and conn['direction'] == 'FROM']
    
    analysis = {
        'station': train_data.get('station', ''),
        'total_connections': len(ber_connections),
        'buses_to': len(buses_to_ber),
        'trains_to': len(trains_to_ber),
        'buses_from': len(buses_from_ber),
        'trains_from': len(trains_from_ber),
        'replaced_by_bus': len(buses_to_ber) > 0 and len(trains_to_ber) == 0,
        'all_connections': ber_connections,
        'buses_to_details': buses_to_ber,
        'trains_to_details': trains_to_ber
    }
    
    return analysis
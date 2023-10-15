from datetime import datetime, timedelta

def convert_time_string(time_string):
    now = datetime.now()
    if time_string == "None":
        return None

    if 'minute' in time_string:
        minutes = int(time_string[0])
        return (now - timedelta(minutes=minutes)).isoformat()
        
    if 'hour' in time_string:
        hours = int(time_string[0])
        return (now - timedelta(hours=hours)).isoformat()

    if 'yesterday' in time_string:
        return (now - timedelta(days=1)).isoformat()
        
    if 'day' in time_string:
        days = int(time_string[0])
        return (now - timedelta(days=days)).isoformat()
    
    if 'month' in time_string:
        return (now - timedelta(days=30)).isoformat()

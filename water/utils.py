from datetime import datetime

def nanoseconds_to_minutes(nanoseconds):
    # Convert nanoseconds to seconds
    seconds = nanoseconds / 1e9

    # Convert to a datetime object
    dt_object = datetime.utcfromtimestamp(seconds)

    # Extract the minute of the hour
    minute_of_hour = dt_object.minute

    return minute_of_hour
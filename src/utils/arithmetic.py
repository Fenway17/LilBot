def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds


# convert seconds into hours, minutes and seconds
def stringify_hrs_mins_secs(seconds) -> str:
    hours, minutes, seconds = convert_seconds(seconds)
    result_string = ""
    if hours != 0:
        result_string = result_string + str(hours) + " hrs "
    if minutes != 0 or hours != 0:
        result_string = result_string + str(minutes) + " mins "
    result_string = result_string + str(seconds) + " secs"
    return result_string

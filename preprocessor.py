import re
import pandas as pd
from datetime import datetime

# Regex pattern that matches both DD/MM/YYYY and MM/DD/YY with AM/PM time
pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APap][Mm]) - '

def try_parse_date(date_str):
    """Attempts to parse date using known formats."""
    formats = [
        "%d/%m/%Y, %I:%M %p",
        "%m/%d/%y, %I:%M %p"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return pd.NaT

def preprocess(data):
    # Split messages using the pattern
    messages = re.split(pattern, data)[1:]

    dates = []
    contents = []

    # Group by threes: [date, time, message], [date, time, message], ...
    for i in range(0, len(messages) - 2, 3):
        date_part = messages[i].strip()
        time_part = messages[i+1].strip()
        message = messages[i+2].strip()

        full_datetime_str = f"{date_part}, {time_part}"
        parsed_date = try_parse_date(full_datetime_str)

        dates.append(parsed_date)
        contents.append(message)

    # Create DataFrame
    df = pd.DataFrame({'message_date': dates, 'message': contents})

    # Remove rows where date parsing failed
    df.dropna(subset=['message_date'], inplace=True)

    # Extract sender (if present)
    users = []
    messages = []

    for msg in df['message']:
        entry = re.split(r'([\w\W]+?):\s', msg, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df['date'] = df['message_date']
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Period column (hour buckets)
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df

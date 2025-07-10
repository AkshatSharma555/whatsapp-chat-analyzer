import re
import pandas as pd

def preprocess(data):
    # Regex for datetime format like: 12/12/2023, 14:32 -
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) != len(dates):
        raise ValueError("Mismatch between number of messages and timestamps. File might be corrupted or formatted differently.")

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean & convert message_date
    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=False)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M', errors='coerce')

    # Drop rows where datetime parsing failed
    df = df.dropna(subset=['message_date'])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract components safely
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Time periods
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df

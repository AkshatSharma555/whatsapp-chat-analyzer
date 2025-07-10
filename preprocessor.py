import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Try multiple timestamp patterns
    patterns = [
        r'\[?(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)\]?\s?[-–]?\s',  # Matches most Android/iPhone formats
    ]

    for pattern in patterns:
        try:
            messages = re.split(pattern, data)[1:]
            if not messages:
                continue  # Try next pattern if nothing matched

            # Group into tuples of (date, time, message)
            chat_data = []
            for i in range(0, len(messages), 3):
                date_str = messages[i].strip()
                time_str = messages[i + 1].strip()
                message = messages[i + 2].strip()

                full_str = f"{date_str}, {time_str}"

                # Try multiple datetime formats
                dt_obj = None
                for fmt in ("%d/%m/%Y, %H:%M", "%d/%m/%Y, %I:%M %p", "%d/%m/%y, %I:%M %p", "%d/%m/%y, %H:%M"):
                    try:
                        dt_obj = datetime.strptime(full_str, fmt)
                        break
                    except:
                        continue
                if dt_obj:
                    chat_data.append((dt_obj, message))
            if not chat_data:
                continue

            # Build dataframe
            df = pd.DataFrame(chat_data, columns=['date', 'user_message'])

            # Split users and messages
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

            # Add time features
            df['only_date'] = df['date'].dt.date
            df['year'] = df['date'].dt.year
            df['month_num'] = df['date'].dt.month
            df['month'] = df['date'].dt.month_name()
            df['day'] = df['date'].dt.day
            df['day_name'] = df['date'].dt.day_name()
            df['hour'] = df['date'].dt.hour
            df['minute'] = df['date'].dt.minute

            # Add period column
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

        except Exception as e:
            continue

    raise ValueError("❌ Failed to preprocess file: Unknown chat format.")

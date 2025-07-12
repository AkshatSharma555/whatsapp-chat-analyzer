import pandas as pd
import re

def classify_message_type(text):
    text = str(text).strip().lower()

    if text.startswith("forwarded") or "forwarded" in text:
        return "Forwarded"
    elif text.endswith("?") or "?" in text:
        return "Question"
    elif re.match(r'^(please|kindly|do|send|give|fill|submit)\b', text):
        return "Command"
    else:
        return "Statement"

def add_message_type_column(df):
    df['message_type'] = df['message'].apply(classify_message_type)
    return df

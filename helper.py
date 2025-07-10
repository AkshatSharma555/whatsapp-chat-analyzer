from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os

extract = URLExtract()

# --- Load Stop Words Safely ---
STOP_WORDS_FILE = "stop_hinglish.txt"
if os.path.exists(STOP_WORDS_FILE):
    with open(STOP_WORDS_FILE, "r", encoding="utf-8") as f:
        stop_words = set(f.read().split())
else:
    stop_words = set()  # Empty fallback set
    print("Warning: stop_hinglish.txt not found. WordCloud and common words may be inaccurate.")

# --- Utility Functions ---

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = sum(len(message.split()) for message in df['message'].dropna())

    num_media_messages = df[df['message'] == '<Media omitted>\\n'].shape[0]

    links = []
    for message in df['message'].dropna():
        links.extend(extract.find_urls(message))

    return num_messages, words, num_media_messages, len(links)

def most_busy_users(df):
    top_users = df['user'].value_counts().head()
    user_percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    user_percent_df.columns = ['name', 'percent']
    return top_users, user_percent_df

def remove_stop_words(message):
    return " ".join([word for word in message.lower().split() if word not in stop_words])

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\\n')]
    temp['message'] = temp['message'].dropna().apply(remove_stop_words)

    text = temp['message'].str.cat(sep=" ")

    if not text.strip():
        return None  # No text to generate wordcloud

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\\n')]

    words = []
    for message in temp['message'].dropna():
        words.extend([word for word in message.lower().split() if word not in stop_words])

    if not words:
        return pd.DataFrame()  # Return empty DataFrame

    return pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message'].dropna():
        emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap

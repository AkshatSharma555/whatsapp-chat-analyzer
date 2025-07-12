import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from helper import extract_topics
from ml.message_type import add_message_type_column




# --- Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="WhatsApp Chat Analytics Dashboard 💬📊",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --- Enhanced CSS for App and Sidebar ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
    color: #263238;
}
.stApp { background-color: #f5f7fa; }

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
    color: #f1f5f9;
    padding: 2rem;
}

/* Force all text inside sidebar to white */
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* File Uploader Style */
div[data-testid="stFileUploaderDropzone"] {
    background-color: #334155;
    border: 2px dashed #00bcd4;
    color: #f1f5f9;
}
div[data-testid="stFileUploaderDropzone"] * {
    color: #f1f5f9 !important;
}
div[data-testid="stFileUploaderDropzone"]:hover {
    background-color: #475569;
    border-color: #00acc1;
}

/* File Uploader Browse Button */
button[kind="secondary"] {
    background-color: #00bcd4 !important;
    color: white !important;
    font-weight: 600;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    border: none;
}
button[kind="secondary"]:hover {
    background-color: #0097a7 !important;
}

/* Dropdown select (visible & options) fix */
div[data-baseweb="select"] {
    background-color: #334155 !important;
    color: #f1f5f9 !important;
    border-radius: 6px;
}
div[data-baseweb="select"] * {
    color: #f1f5f9 !important;
}
ul[role="listbox"] {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #00bcd4;
}
ul[role="listbox"] li {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
}
ul[role="listbox"] li:hover {
    background-color: #00bcd4 !important;
    color: #1e293b !important;
}

/* Sidebar Info Box */
section[data-testid="stSidebar"] .stAlert {
    background-color: #334155 !important;
    color: #f1f5f9 !important;
    border-left: 4px solid #00bcd4;
}

/* Button Styling */
.stButton > button {
    background-color: #00796b;
    color: white;
    font-weight: 600;
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    background-color: #004d40;
    transform: scale(1.02);
}

/* Metric Cards */
.metric-card {
    background-color: white;
    border-radius: 10px;
    padding: 1.2rem;
    margin: 0.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    border-left: 5px solid #00796b;
}
.metric-card h3 {
    color: #455a64;
    font-size: 1rem;
    margin-bottom: 0.3rem;
    font-weight: 600;
}
.metric-card .st-emotion-cache-nahz7x.e1nzilvr4 {
    color: #004d40;
    font-size: 2.2rem;
    font-weight: 700;
    margin-top: 0.5rem;
}

/* Chart Container */
.st-emotion-cache-16cq8s0.e1nzilvr5 {
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

/* Links */
a {
    color: #00bcd4;
}
a:hover {
    text-decoration: underline;
}
/* Fix for long user dropdown (scrollable select box) */
ul[role="listbox"] {
    max-height: 250px !important;
    overflow-y: auto !important;
    scrollbar-width: thin;
    scrollbar-color: #00bcd4 #1e293b;
}
ul[role="listbox"]::-webkit-scrollbar {
    width: 6px;
}
ul[role="listbox"]::-webkit-scrollbar-thumb {
    background-color: #00bcd4;
    border-radius: 4px;
}
ul[role="listbox"]::-webkit-scrollbar-track {
    background-color: #1e293b;
}

/* Optional: make sidebar scrollable if content is too long */
section[data-testid="stSidebar"] > div {
    max-height: 90vh;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)


# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #00796b;'> WhatsApp Chat Analytics Dashboard 💬📊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #455a64;'>Uncover fascinating insights and statistics from your WhatsApp conversations!</p>", unsafe_allow_html=True)
st.markdown("---") # Horizontal line for visual separation

# --- Sidebar Content ---
with st.sidebar:
    st.title("Upload & Select 📂")
    st.markdown("---")
    st.markdown("Upload your exported **WhatsApp chat file** (.txt) below to begin your analysis journey!")

    uploaded_file = st.file_uploader("📂 Choose a chat file", type=["txt"])

    if uploaded_file is not None:
        with st.spinner("🚀 Processing your chat... This might take a moment!"):
            try:
                bytes_data = uploaded_file.getvalue()
                data = bytes_data.decode("utf-8")
                df = preprocessor.preprocess(data)

                st.success("✅ File uploaded and processed successfully!")

                # Fetch unique users
                user_list = df['user'].unique().tolist()
                if 'group_notification' in user_list:
                    user_list.remove('group_notification')
                user_list.sort()
                user_list.insert(0, "Overall")

                selected_user = option_menu(
                    menu_title="👤 Show analysis for:",
                    options=user_list,
                    icons=["person"] * len(user_list),
                    default_index=0,
                    orientation="vertical",
                    styles={
                        "container": {"padding": "0.5rem", "background-color": "#1e293b"},
                        "nav-link": {"font-size": "1rem", "color": "#f1f5f9", "text-align": "left"},
                        "nav-link-selected": {"background-color": "#00bcd4", "color": "#1e293b", "font-weight": "bold"},
                    }
                )

                st.markdown("---")
                if st.button("✨ Show Analysis", help="Click to display the chat analysis for the selected user or overall group."):
                    st.session_state['show_analysis'] = True
                    st.session_state['selected_user'] = selected_user
                    st.session_state['df'] = df
                else:
                    st.session_state['show_analysis'] = False

            except Exception as e:
                st.error(f"⚠️ Oops! There was an error processing your file. Please ensure it's a valid WhatsApp chat export. Error: {e}")
                st.info("💡 **Tip:** Make sure your chat export is unencrypted and in the standard text format. Try exporting 'Without Media'.")
    else:
        st.info("⬆️ **Please upload a chat file from the sidebar to begin analysis.**")
        st.markdown("""
        ---
        ### How to Export Your WhatsApp Chat:
        1.  Open the chat you want to analyze.
        2.  Tap on the three dots (More options) -> **More** -> **Export chat**.
        3.  Choose "**Without Media**" for a smaller file size and faster processing.
        4.  Select a method to save the .txt file to your device (e.g., Gmail, Drive, etc.).
        """)

# --- Main Content Area (Conditional Display) ---
if 'show_analysis' in st.session_state and st.session_state['show_analysis']:
    selected_user = st.session_state['selected_user']
    df = st.session_state['df']

    st.markdown(f"## Unveiling Insights for: <span style='color:#00796b;'>{selected_user}</span>", unsafe_allow_html=True)
    st.markdown("---")

    # --- Top Statistics Section ---
    st.markdown("### Key Metrics 📈")
    st.markdown("Here's a quick overview of the chat's activity:")

    # Use a container for metric cards for better layout control
    with st.container(border=True): # New feature in Streamlit 1.29+
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Messages</h3>
                <p class="st-emotion-cache-nahz7x e1nzilvr4">{num_messages}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Words</h3>
                <p class="st-emotion-cache-nahz7x e1nzilvr4">{words}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Media Shared</h3>
                <p class="st-emotion-cache-nahz7x e1nzilvr4">{num_media_messages}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Links Shared</h3>
                <p class="st-emotion-cache-nahz7x e1nzilvr4">{num_links}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

    # --- Monthly Timeline ---
    st.subheader("Monthly Activity Trend 🗓️")
    st.markdown("Observe the message frequency over time to identify peak periods.")
    timeline = helper.monthly_timeline(selected_user, df)
    fig_monthly, ax_monthly = plt.subplots(figsize=(12, 5))
    ax_monthly.plot(timeline['time'], timeline['message'], color='#26A69A', linewidth=2) # Teal line
    ax_monthly.set_xlabel("Month", fontsize=12)
    ax_monthly.set_ylabel("Number of Messages", fontsize=12)
    ax_monthly.set_title("Monthly Message Timeline", fontsize=14, weight='bold', color='#00695C')
    plt.xticks(rotation='vertical', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_monthly)
    st.markdown("---")

    # --- Daily Timeline ---
    st.subheader("Daily Activity Trend ☀️")
    st.markdown("Understand the daily message flow and busiest days of the week.")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig_daily, ax_daily = plt.subplots(figsize=(12, 5))
    ax_daily.plot(daily_timeline['only_date'], daily_timeline['message'], color='#424242', linewidth=2) # Dark Grey line
    ax_daily.set_xlabel("Date", fontsize=12)
    ax_daily.set_ylabel("Number of Messages", fontsize=12)
    ax_daily.set_title("Daily Message Timeline", fontsize=14, weight='bold', color='#00695C')
    plt.xticks(rotation='vertical', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig_daily)
    st.markdown("---")

    # --- Activity Map ---
    st.subheader("Activity Hotspots 🗓️⏰")
    st.markdown("Discover the most active days of the week and months.")
    col_day_month1, col_day_month2 = st.columns(2)

    with col_day_month1:
        st.markdown("### Most Busy Days 📆")
        busy_day = helper.week_activity_map(selected_user, df)
        fig_busy_day, ax_busy_day = plt.subplots(figsize=(8, 5))
        ax_busy_day.bar(busy_day.index, busy_day.values, color='#9C27B0') # Purple
        ax_busy_day.set_xlabel("Day of Week", fontsize=12)
        ax_busy_day.set_ylabel("Number of Messages", fontsize=12)
        ax_busy_day.set_title("Most Busy Days of the Week", fontsize=14, weight='bold', color='#00695C')
        plt.xticks(rotation='vertical', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_busy_day)

    with col_day_month2:
        st.markdown("### Most Busy Months 📅")
        busy_month = helper.month_activity_map(selected_user, df)
        fig_busy_month, ax_busy_month = plt.subplots(figsize=(8, 5))
        ax_busy_month.bar(busy_month.index, busy_month.values, color='#FF9800') # Orange
        ax_busy_month.set_xlabel("Month", fontsize=12)
        ax_busy_month.set_ylabel("Number of Messages", fontsize=12)
        ax_busy_month.set_title("Most Busy Months", fontsize=14, weight='bold', color='#00695C')
        plt.xticks(rotation='vertical', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_busy_month)
    st.markdown("---")

    st.subheader("Weekly Activity Heatmap ⚡")
    st.markdown("Identify patterns of activity across days and hours.")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(14, 8))
    sns.heatmap(user_heatmap, ax=ax_heatmap, cmap='viridis', annot=True, fmt=".0f", linewidths=.5, linecolor='white')
    ax_heatmap.set_xlabel("Time of Day", fontsize=12)
    ax_heatmap.set_ylabel("Day of Week", fontsize=12)
    ax_heatmap.set_title("Message Activity Heatmap", fontsize=16, weight='bold', color='#00695C')
    st.pyplot(fig_heatmap)
    st.markdown("---")

    # --- SENTIMENT ANALYSIS SECTION ---
    st.subheader("Sentiment Analysis 🧠")
    st.markdown("Every message has a mood. Let’s see how this chat feels...")

    # Ensure 'sentiment' column exists
    if 'sentiment' not in df.columns:
        from ml import sentiment

        df = sentiment.add_sentiment_column(df)
        st.session_state['df'] = df  # Save back to session state for further use

    sentiment_counts = df['sentiment'].value_counts()
    sentiment_labels = ['Positive', 'Neutral', 'Negative']
    sentiment_colors = ['#43a047', '#fdd835', '#e53935']
    sentiment_values = [sentiment_counts.get(s, 0) for s in sentiment_labels]

    fig_sentiment, ax_sentiment = plt.subplots()
    ax_sentiment.pie(sentiment_values, labels=sentiment_labels, autopct='%1.1f%%',
                     colors=sentiment_colors, startangle=90)
    ax_sentiment.axis('equal')
    ax_sentiment.set_title("Sentiment Distribution", fontsize=14, weight='bold', color='#00695C')
    st.pyplot(fig_sentiment)
    st.markdown("---")

    # --- TOPIC MODELING SECTION ---
    st.subheader("Topic Modeling 🧠📚")
    st.markdown("Explore the major themes being discussed in this chat!")

    topics = extract_topics(df)

    if not topics:
        st.info("Not enough data to extract topics. Try selecting a different user or a larger chat.")
    else:
        for idx, (topic_title, words) in enumerate(topics):
            styled_words = " ".join([
                                        f"<span style='background-color:#e0f7fa; color:#00695C; padding:4px 8px; margin:3px; border-radius:8px; display:inline-block;'>{word}</span>"
                                        for word in words])

            st.markdown(f"""
                <div style="background-color:#f1f8e9; padding:20px; border-radius:12px; margin-bottom:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
                    <h4 style='color:#2e7d32;'>🧠 Topic {idx + 1}</h4>
                    <p>{styled_words}</p>
                </div>
            """, unsafe_allow_html=True)

    # --- Message Type Classification with Side Legend (Fixed Overlapping Percentages) ---
    if 'message_type' not in df.columns:
        df = add_message_type_column(df)
        st.session_state['df'] = df

    st.subheader("Message Type Classification 🧾")
    st.markdown("Explore the nature of messages – questions, statements, commands, or forwards.")

    msg_type_counts = df['message_type'].value_counts()
    labels = msg_type_counts.index.tolist()
    sizes = msg_type_counts.values.tolist()
    colors = sns.color_palette("Set2", len(labels))

    # Pie chart without percentages on the chart
    fig_type, ax_type = plt.subplots(figsize=(8, 6))
    wedges, _ = ax_type.pie(
        sizes,
        startangle=90,
        colors=colors,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        labels=None,  # No inline labels
        autopct=None
    )
    ax_type.axis('equal')
    ax_type.set_title("Message Type Breakdown", fontsize=14, weight='bold', color='#00695C')

    # Show percentages in the legend instead
    total = sum(sizes)
    if total > 0:
        legend_labels = [f"{label}: {round((count / total) * 100, 1)}%" for label, count in zip(labels, sizes)]
    else:
        legend_labels = [f"{label}: 0%" for label in labels]

    ax_type.legend(
        handles=wedges,
        labels=legend_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=12,
        title="Message Types",
        title_fontsize=13
    )

    st.pyplot(fig_type)

    # --- USER CLUSTERING SECTION ---
    st.subheader("User Clustering 🔍")
    st.markdown(
        "Discover groups of users with similar behavior based on message length, emoji use, sentiment, and more.")

    from ml.user_cluster import extract_user_features, cluster_users

    if selected_user == "Overall":
        user_features = extract_user_features(df)
        clustered = cluster_users(user_features, n_clusters=3)

        col_cluster1, col_cluster2 = st.columns([2, 1])

        with col_cluster1:
            import seaborn as sns

            fig_cluster, ax_cluster = plt.subplots(figsize=(10, 6))
            sns.scatterplot(
                x='pca1', y='pca2',
                hue='cluster',
                data=clustered,
                palette='Set2',
                s=100,
                ax=ax_cluster
            )
            for i, row in clustered.iterrows():
                ax_cluster.text(row['pca1'] + 0.02, row['pca2'] + 0.02, i, fontsize=9)
            ax_cluster.set_title("User Clusters (PCA View)", fontsize=14, weight='bold', color='#00695C')
            st.pyplot(fig_cluster)

        with col_cluster2:
            st.markdown("### Cluster Summary Table:")
            cluster_summary = clustered[['total_messages', 'avg_msg_length', 'emoji_usage', 'cluster']].copy()
            cluster_summary['cluster'] = cluster_summary['cluster'].astype(str)
            st.dataframe(cluster_summary.style.set_properties(**{'font-size': '1rem'}), use_container_width=True)
    else:
        st.info("Switch to **Overall** to view user-level clustering.")

    # --- USER CLUSTERING ---
    st.subheader("User Clustering 🔍")
    st.markdown("Discover groups of users with similar message content.")

    from ml.user_clustering import cluster_users

    users, labels, cluster_map = cluster_users(df)

    if cluster_map:
        for cluster, members in cluster_map.items():
            st.markdown(f"**{cluster}:** " + ", ".join(members))
    else:
        st.warning("Not enough data to form clusters. Try with a bigger group or more users.")

    # --- Busiest Users (Group Level) ---
    if selected_user == 'Overall':
        st.subheader("Top Contributors (Group Chat) 👥")
        st.markdown("See who's leading the conversation in this group chat.")
        x, new_df = helper.most_busy_users(df)
        fig_busiest_users, ax_busiest_users = plt.subplots(figsize=(10, 6))

        col_busiest1, col_busiest2 = st.columns(2)

        with col_busiest1:
            ax_busiest_users.bar(x.index, x.values, color='#D32F2F') # Red
            ax_busiest_users.set_xlabel("User", fontsize=12)
            ax_busiest_users.set_ylabel("Number of Messages", fontsize=12)
            ax_busiest_users.set_title("Most Busy Users", fontsize=14, weight='bold', color='#00695C')
            plt.xticks(rotation='vertical', fontsize=10)
            plt.yticks(fontsize=10)
            plt.tight_layout()
            st.pyplot(fig_busiest_users)
        with col_busiest2:
            st.markdown("### Message Share Breakdown:")
            st.dataframe(new_df.style.set_properties(**{'font-size': '1.05rem', 'text-align': 'left'}), use_container_width=True) # Better styling for dataframe

    st.markdown("---")

    # --- WordCloud ---
    st.subheader("Most Frequent Words (Word Cloud) ☁️")
    st.markdown("A visual representation of the most commonly used words in the chat.")
    df_wc = helper.create_wordcloud(selected_user, df)
    if df_wc is not None:
        fig_wc, ax_wc = plt.subplots(figsize=(12, 6))
        ax_wc.imshow(df_wc, interpolation='bilinear')
        ax_wc.axis("off") # Hide axes
        st.pyplot(fig_wc)
    else:
        st.info("No meaningful words found to generate a WordCloud (possibly only media or system messages).")
    st.markdown("---")

    # --- Most Common Words ---
    st.subheader("Top 20 Most Common Words 📝")
    st.markdown("Discover the words that dominate your conversations.")
    most_common_df = helper.most_common_words(selected_user, df)
    if not most_common_df.empty:
        fig_common_words, ax_common_words = plt.subplots(figsize=(10, 8))
        sns.barplot(x=most_common_df['count'], y=most_common_df['word'], ax=ax_common_words, palette='GnBu_r')
        ax_common_words.set_xlabel("Frequency", fontsize=12)
        ax_common_words.set_ylabel("Word", fontsize=12)
        ax_common_words.set_title("Most Common Words", fontsize=14, weight='bold', color='#00695C')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_common_words)
    else:
        st.info("Not enough textual data to find common words.")
    st.markdown("---")

    # --- Emoji Analysis ---
if 'selected_user' in st.session_state and 'df' in st.session_state:
    selected_user = st.session_state['selected_user']
    df = st.session_state['df']

    st.subheader("Emoji Usage Analysis 😂❤️👍")
    st.markdown("Which emojis are used most frequently?")

    emoji_df = helper.emoji_helper(selected_user, df)

    if not emoji_df.empty:
        col_emoji1, col_emoji2 = st.columns(2)

        with col_emoji1:
            st.markdown("### Top Emojis Table:")
            st.dataframe(
                emoji_df.style.set_properties(**{'font-size': '1.05rem', 'text-align': 'left'}),
                use_container_width=True
            )

        with col_emoji2:
            st.markdown("### Emoji Distribution:")

            # --- Set cross-platform emoji font ---
            import platform

            if platform.system() == "Windows":
                plt.rcParams['font.family'] = 'Segoe UI Emoji'
            elif platform.system() == "Darwin":
                plt.rcParams['font.family'] = 'Apple Color Emoji'
            else:
                plt.rcParams['font.family'] = 'Noto Color Emoji'

            # --- Create pie chart ---
            fig_emoji_pie, ax_emoji_pie = plt.subplots(figsize=(8, 8))

            top_n = 5 if len(emoji_df) >= 5 else len(emoji_df)
            counts = emoji_df['count'].head(top_n)
            labels = emoji_df['emoji'].head(top_n)

            ax_emoji_pie.pie(
                counts,
                labels=labels,
                autopct="%0.2f%%",
                startangle=90,
                colors=sns.color_palette("Set2")
            )
            ax_emoji_pie.set_title("Top Emoji Distribution", fontsize=14, weight='bold', color='#00695C')
            st.pyplot(fig_emoji_pie)
    else:
        st.info("No emojis found in this chat.")
    st.markdown("---")

# --- Footer ---
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #b2dfdb; color: #607d8b;">
    Crafted with purpose and precision by <strong>Akshat Sharma</strong>
    <br>
    <small>Experience the story behind your chats — one message at a time.</small>
    <br>
    <small style="font-size: 0.85rem;">100% privacy-focused: Your data never leaves your device.</small>
</div>
""", unsafe_allow_html=True)
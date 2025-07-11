# whatsapp-chat-analyzer

A powerful and privacy-focused Streamlit app that uncovers meaningful insights from your WhatsApp conversations — be it personal chats or group discussions. Built with Python, Pandas, Matplotlib, Seaborn, and love 💚

🔗 [Live Demo on Streamlit](https://whatsapp-chat-analyzer-nvh5sfm45pwjntt3vpgvkk.streamlit.app)  
---

## 📌 What This App Does

This app allows you to upload your exported WhatsApp `.txt` chat file and provides:

- 📈 Key statistics (messages, words, media, links)
- 📅 Activity trends (monthly, daily)
- 📊 Active days and times
- ☁️ Word clouds and most common words
- 😂 Emoji usage analytics
- 👥 Individual + Group analysis
- 🎨 Interactive charts and beautiful UI

Works seamlessly for:
- ✅ One-on-one personal chats
- ✅ Group chats (with per-user and overall stats)

---

## 🎯 Key Features

| Feature                        | Description |
|-------------------------------|-------------|
| 📈 **Key Metrics Dashboard**  | See total messages, word count, media and link stats |
| 📅 **Monthly Activity Trend** | Track chat activity month-wise with line chart |
| 📆 **Daily Activity Trend**   | Understand how active the chat is on a daily basis |
| 📊 **Activity Hotspots**      | Bar charts of busiest weekdays and months |
| ⚡ **Weekly Heatmap**         | See which day and hour people are most active |
| 👥 **Top Contributors**       | In group chats, see who chats the most |
| ☁️ **Word Cloud**             | Visual cloud of most used words (after cleaning) |
| 📝 **Top 20 Words**           | Exact word frequency breakdown |
| 😂 **Emoji Analysis**         | Emoji counts with table + pie chart |


## 🔐 Privacy First – Always

✔️ No data is uploaded, stored, or shared.  
✔️ All processing happens in-memory (locally in browser + Streamlit session).  
✔️ You can verify this by reading the source code.  
🛡️ Your data is **never** stored in any database or server.

---

## 📂 How to Export WhatsApp Chat

1. Open a WhatsApp chat  
2. Tap the 3-dot menu → **More** → **Export Chat**  
3. Choose **Without Media**  
4. Send the `.txt` file to your device (via Gmail, Drive, etc.)

---

## 🚀 Run Locally (for Developers)

### ⚙️ Requirements

- Python 3.8+
- pip packages:
  ```bash
  pip install streamlit matplotlib seaborn wordcloud pandas urlextract emoji
  streamlit run app.py

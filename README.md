<div align="center">
  <h2 align="center">Telegram Message Forwarder</h2>
  <p align="center">
    An automated tool for forwarding Telegram messages from a source to multiple destinations, with support for topics, scheduled forwarding, and rate limiting. Made with ai so do not mind the shitty codebase
    <br />
    <br />
    <a href="#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Telegram-Advertiser/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Telegram-Advertiser/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Automated Telegram message forwarding
- Support for forwarding to multiple destinations
- Topic support for group chats (forward to specific topics)
- Two modes: 'once' for single execution or 'daily' for scheduled forwarding
- Configurable delay between forwards to avoid rate limits
- Ignore on error for specific destinations
- Session management with Telethon
- Comprehensive logging with logmagix
- Error handling and warnings for failed forwards
- Configurable via YAML file

---

### 📝 Usage

1. **Configuration**:
   Edit `input/config.yaml`:

   ```yaml
   # config.yaml
   telegram:
     api_id: YOUR_API_ID # GET FROM: https://my.telegram.org
     api_hash: "YOUR_API_HASH" # GET FROM: https://my.telegram.org
     session_name: "message_forwarder"

   forwarder:
     mode: "daily" # Options: "once" or "daily"
     source_message: "https://t.me/channel/123" # Link to the message to forward

     destinations:
       - "https://t.me/dest1"
       - "https://t.me/dest2/456" # With topic ID
       - "https://t.me/dest3"

     ignore_on_error: # Destinations to ignore if forwarding fails
       - "https://t.me/dest3"

     daily_refresh_hours: 12 # For daily mode, run every 12 hours
     delay_between_forwards: 5 # Seconds delay between each forward

   logging:
     level: "INFO"
     show_colors: true
     show_time: true
   ```

   - Obtain `api_id` and `api_hash` from [https://my.telegram.org](https://my.telegram.org)
   - Set the `source_message` to the Telegram link of the message you want to forward (e.g., https://t.me/channel/123)
   - Add destination links in the `destinations` list. For topics, append the topic ID (e.g., /456)
   - Optionally, add destinations to `ignore_on_error` list to skip them if forwarding fails (logs as warning instead of error)
   - Choose mode: "once" for one-time forward, "daily" for repeated forwarding
   - Adjust `daily_refresh_hours` for the interval in daily mode
   - Set `delay_between_forwards` to add pauses between forwards

2. **Running the script**:

   ```bash
   python main.py
   ```

3. **Output**:
   - The script will log the forwarding process
   - In daily mode, it will continue running and forward at the specified intervals
   - Session files are created for authentication

---

### 📹 Preview

![Preview](https://i.imgur.com/leCy91D.png)

---

### ❗ Disclaimers

- This project is for educational purposes only
- The author is not responsible for any misuse of this tool
- Use responsibly and in accordance with Telegram's terms of service
- Ensure you have permission to forward messages to the destinations

---

### 📜 ChangeLog

```diff
v1.0.0 ⋮ 01/28/2026
! Initial release of Telegram Message Forwarder.
+ Added support for topic forwarding
+ Implemented daily and once modes
+ Added configurable delays and logging
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Telegram-Advertiser.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Telegram-Advertiser.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Telegram-Advertiser.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>

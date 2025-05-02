# 🏝️ Malta Public Holiday Notifier for Microsoft Teams

This Python script checks daily whether the current date is a **public holiday in Malta**, and sends a message to a Microsoft Teams channel via a webhook integration.

- ✅ Posts a clear "Yes" or "No" message
- 🟥 Red background if today **is** a public holiday
- 🟩 Green background if today **is not**
- 🕗 Intended to be run automatically via a cronjob (e.g., daily at 8:00am BST)

---

## 🚀 Features

- Uses the `holidays` library to determine Maltese public holidays
- Sends an Adaptive Card to Microsoft Teams with styled output
- Supports `.env` configuration for secure webhook handling

---

## 🧱 Requirements

- Python 3.7+
- A Microsoft Teams incoming webhook URL
- A Linux-based scheduler (e.g., `cron`) or task runner

---

## 🔧 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/malta-holiday-notifier.git
cd malta-holiday-notifier
```

2. **Create a .env file:**

```bash
WEBHOOK_URL=https://your-teams-webhook-url
```

> [!TIP]
> You can get your webhook URL by adding the **Incoming Webhook** connector to a Teams channel.

3. **Install dependencies:**

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, create it:

```bash
holidays
requests
python-dotenv
```

## Running automatically with Cron

To run daily at 9:00am BST Monday to Friday, add this line to your crontab:

```bash
0 8 * * 1-5 cd /path/to/script_directory && ./venv/bin/python holiday_checker.py >> /path/to/script_directory/cron.log 2>&1
```

Or use a shell script wrapper that loads the `.env` file:

```bash
#!/bin/bash
cd /path/to/script
export $(grep -v '^#' .env | xargs)
python3 holiday_checker.py
```

Make it executable and update your crontab accordingly.

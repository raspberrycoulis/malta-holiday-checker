import datetime
import requests
import holidays
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TITLE = "Is it a public holiday in Malta today?"

def is_public_holiday_in_malta(today):
    mt_holidays = holidays.MT()
    return today in mt_holidays, mt_holidays.get(today)

def send_teams_message(is_holiday, holiday_name):
    message = "Yes" if is_holiday else "No"
    details = f"Today is {holiday_name}. ClamTech are probably not working today!" if holiday_name else "Today is not a public holiday in Malta, so ClamTech should be working today."
    style = "attention" if is_holiday else "good"  # Red or green background container

    # Console log for cron tracking
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"[{timestamp}] Result: {message}. {details}")

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "Container",
                            "style": style,
                            "bleed": True,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": TITLE,
                                    "wrap": True,
                                    "size": "Large",
                                    "weight": "Bolder",
                                    "horizontalAlignment": "Center"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": message,
                                    "wrap": True,
                                    "spacing": "Medium",
                                    "size": "ExtraLarge",
                                    "weight": "Bolder",
                                    "horizontalAlignment": "Center"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": details,
                                    "wrap": True,
                                    "spacing": "Small",
                                    "isSubtle": True,
                                    "horizontalAlignment": "Center"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()

def main():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"[{timestamp}] Script started.")

    today = datetime.date.today()
    holiday_today, holiday_name = is_public_holiday_in_malta(today)
    send_teams_message(holiday_today, holiday_name)

if __name__ == "__main__":
    main()

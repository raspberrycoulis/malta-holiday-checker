## This version only sends a Teams message if it is a public holiday in Malta.

import datetime
import requests
import holidays
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TITLE = "Is it a public holiday in Malta today?"

def is_public_holiday_in_malta(date_to_check):
    mt_holidays = holidays.MT()
    name = mt_holidays.get(date_to_check)
    return bool(name), name

def send_teams_message(is_holiday, holiday_name):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    message = "Yes"
    details = f"Today is {holiday_name}. ClamTech are probably not working today!"
    style = "attention" # Red background container for holiday

    # Console log for cron tracking
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
    is_holiday, holiday_name = is_public_holiday_in_malta(today)

    if is_holiday:
        send_teams_message(holiday_name)
    else:
        print(f"[{timestamp}] Not a public holiday in Malta today ({today}). No Teams message sent.")

if __name__ == "__main__":
    main()

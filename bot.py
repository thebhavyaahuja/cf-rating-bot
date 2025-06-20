import requests
import smtplib
import time
import os
from configparser import ConfigParser
from email.mime.text import MIMEText

LAST_NOTIFIED_FILE = 'last_notified.txt'

# Load user configuration and secrets
def load_config():
    config = ConfigParser()
    config.read('config.ini')
    return {
        'handle': os.environ['HANDLE'],
        'recipient_email': os.environ['EMAIL'],
        'smtp_server': config.get('EMAIL', 'smtp_server'),
        'smtp_port': config.getint('EMAIL', 'smtp_port'),
        'smtp_user': config.get('EMAIL', 'sender_email'),
        'smtp_password': config.get('EMAIL', 'password')
    }

# Get Codeforces rating history
def get_rating(handle):
    url = f'https://codeforces.com/api/user.rating?handle={handle}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Error fetching Codeforces API: {response.status_code}")

# Save last notified time to file
def save_last_notified_time(timestamp):
    with open(LAST_NOTIFIED_FILE, 'w') as f:
        f.write(str(timestamp))

# Load last notified time from file
def load_last_notified_time():
    if not os.path.exists(LAST_NOTIFIED_FILE):
        return 0  # No notifications sent yet
    with open(LAST_NOTIFIED_FILE, 'r') as f:
        return int(f.read().strip())

# Email sender
def send_email_notification(smtp_info, contest_name, old_rating, new_rating):
    rating_change = new_rating - old_rating
    color = "green" if rating_change >= 0 else "red"
    sign = "+" if rating_change >= 0 else ""

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #333;">📊 Contest Update: <span style="color:#0077cc;">{contest_name}</span></h2>
        <p><b>Old Rating:</b> {old_rating}</p>
        <p><b>New Rating:</b> {new_rating}</p>
        <p><b>Rating Change:</b> <span style="color: {color}; font-weight: bold;">{sign}{rating_change}</span></p>
    </body>
    </html>
    """

    msg = MIMEText(html, 'html')
    msg['Subject'] = "Contest Rating Update!"
    msg['From'] = smtp_info['smtp_user']
    msg['To'] = smtp_info['recipient_email']

    with smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port']) as server:
        server.starttls()
        server.login(smtp_info['smtp_user'], smtp_info['smtp_password'])
        server.send_message(msg)

# Main logic
def main():
    config = load_config()
    handle = config['handle']
    smtp_info = {
        'smtp_user': config['smtp_user'],
        'smtp_password': config['smtp_password'],
        'smtp_server': config['smtp_server'],
        'smtp_port': config['smtp_port'],
        'recipient_email': config['recipient_email']
    }

    last_notified_time = load_last_notified_time()

    try:
        ratings = get_rating(handle)
        latest = ratings[-1]
        contest_name = latest['contestName']
        old_rating = latest['oldRating']
        new_rating = latest['newRating']
        rating_update_time = latest['ratingUpdateTimeSeconds']

        print(f"Latest rating: {new_rating} from {contest_name} at {time.ctime(rating_update_time)}")

        if rating_update_time > last_notified_time:
            send_email_notification(smtp_info, contest_name, old_rating, new_rating)
            save_last_notified_time(rating_update_time)
            print("Email sent and timestamp updated.")
        else:
            print("No new rating update.")

    except Exception as e:
        print(f"[Error] {e}")

if __name__ == '__main__':
    main()

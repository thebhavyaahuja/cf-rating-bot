import requests
import smtplib
import time
import os
from configparser import ConfigParser
from email.mime.text import MIMEText

# Load user configuration and fetch environment variables from Github Secrets
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

# Query Codeforces API for user rating
def get_rating(handle):
    url = f'https://codeforces.com/api/user.rating?handle={handle}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Error fetching data from Codeforces API: {response.status_code}")

# Send email notification
def send_email_notification(smtp_info, contest_name, old_rating, new_rating):
    rating_change = new_rating - old_rating

    # Determine color for rating change
    color = "green" if rating_change >= 0 else "red"
    sign = "+" if rating_change >= 0 else ""

    # HTML Message
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

    # Create MIMEText with HTML
    msg = MIMEText(html, 'html')
    msg['Subject'] = "Contest Rating Update!"
    msg['From'] = smtp_info['smtp_user']
    msg['To'] = smtp_info['recipient_email']

    with smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port']) as server:
        server.starttls()
        server.login(smtp_info['smtp_user'], smtp_info['smtp_password'])
        server.send_message(msg)

# Main logic for the bot
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

    last_notified_time = 0

    try:
        ratings = get_rating(handle)
        latest_rating = ratings[-1]
        contest_name = latest_rating['contestName']
        new_rating = latest_rating['newRating']
        rating_update_time = latest_rating['ratingUpdateTimeSeconds']
        print(f"Latest rating for {handle}: {new_rating} (Contest: {contest_name})")
        print(f"Rating update time: {time.ctime(rating_update_time)}")

        if rating_update_time > last_notified_time:
            old_rating = latest_rating['oldRating']
            send_email_notification(smtp_info, contest_name, old_rating, new_rating)
            last_notified_time = rating_update_time

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

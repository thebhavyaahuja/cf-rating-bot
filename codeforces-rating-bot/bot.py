import requests
import smtplib
import time
import os
from configparser import ConfigParser
from email.mime.text import MIMEText
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load email configuration
def load_config():
    config = ConfigParser()
    config.read('config.ini')
    return {
        'smtp_server': config.get('EMAIL', 'smtp_server'),
        'smtp_port': config.getint('EMAIL', 'smtp_port'),
        'smtp_user': config.get('EMAIL', 'sender_email'),
        'smtp_password': config.get('EMAIL', 'password')
    }

# Load users from Google Sheet
def load_users_from_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Codeforces Rating Bot (Responses)").sheet1
    records = sheet.get_all_records()
    print(f"Loaded {len(records)} users from Google Sheet.")
    return records, sheet

# Query Codeforces API for user rating
def get_rating(handle):
    url = f'https://codeforces.com/api/user.rating?handle={handle}'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['result']
        else:
            raise Exception(f"Codeforces API error for handle {handle}: {data.get('comment')}")
    else:
        raise Exception(f"Error fetching data from Codeforces API: {response.status_code}")

# Send email notification
def send_email_notification(smtp_info, recipient_email, contest_name, old_rating, new_rating):
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
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port'], timeout=30) as server:
        server.starttls()
        server.login(smtp_info['smtp_user'], smtp_info['smtp_password'])
        server.send_message(msg)

# Main logic for the bot
def main():
    smtp_info = load_config()
    
    try:
        users, sheet = load_users_from_google_sheet()
        print(f"Loaded {len(users)} users from Google Sheet.")
    except Exception as e:
        print(f"Failed to load users from Google Sheet: {e}")
        return

    total_users = len(users)
    for idx, user in enumerate(users):
        try:
            handle = user['Put in your cf handle']
            email = user['Put in the email address you\'d like to receive notifications on']
            last_notified_time = user['Last Notified Time'] or 0

            print(f"  Fetching ratings for {handle}...")
            ratings = get_rating(handle)
            print(f"  Successfully fetched ratings for {handle}.")

            if not ratings:
                print(f"  No rating history for handle: {handle}")
                continue

            # API returns ratings in chronological order, so the last one is the latest.
            latest_rating = ratings[-1]
            rating_update_time = latest_rating['ratingUpdateTimeSeconds']

            if rating_update_time > last_notified_time:
                old_rating = latest_rating['oldRating']
                new_rating = latest_rating['newRating']
                contest_name = latest_rating['contestName']
                
                print(f"  New rating for {handle}. Sending notification to {email}.")
                send_email_notification(smtp_info, email, contest_name, old_rating, new_rating)
                
                # Update timestamp in Google Sheet. Row is idx + 2 because of 1-based index and header row.
                sheet.update_cell(idx + 2, 4, rating_update_time)
                print(f"Updated last notified timestamp for {handle}.")
            else:
                print(f"No new rating update for {handle}. Last notified time: {last_notified_time}, current time: {rating_update_time}")

        except Exception as e:
            print(f"An error occurred for user {handle}: {e}")
            continue # Continue to the next user

if __name__ == '__main__':
    main()

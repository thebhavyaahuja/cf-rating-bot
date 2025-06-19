# Codeforces Rating Notification Bot

## Introduction
The Codeforces Rating Notification Bot is a personal automation script designed for Codeforces users. It eliminates the need to manually check the Codeforces website for rating updates after contests by providing instant notifications directly to the user's email.

## Features
- **User Configuration**: Easily configure your Codeforces handle and email notification credentials.
- **API Integration**: Automatically queries the Codeforces API to check for rating changes.
- **Notification System**: Sends formatted email notifications when your rating changes.
- **Error Handling**: Gracefully handles potential errors such as API downtime or invalid user handles.

## Installation
1. Clone the repository.

2. Navigate to the project directory:
   ```
   cd cf-rating-bot
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
Create a `config.ini` file in the project directory with the following structure:

```ini
[USER]
handle = your_codeforces_handle

[EMAIL]
recipient_email = your_recipient_email@example.com
sender_email = your_sender_email@example.com
password = your_email_app_password (can be generated from accounts.google using App Passwords)
smtp_server = smtp.example.com
smtp_port = 587
```

Replace the placeholder values with your actual Codeforces handle, email credentials, and SMTP server details. For example, for Gmail, `smtp_server` would be `smtp.gmail.com` and `smtp_port` would be `587`.

## Usage
Run the bot using the following command:
```
python3 bot.py
```

The bot will check for rating updates and send notifications as configured.

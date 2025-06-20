## About

Codeforces doesn’t send notifications (atleast to me) when contest ratings are updated, and results can take anywhere from 2 to 12 hours to appear. This bot checks your rating automatically and emails you the moment it changes — no need to keep refreshing the CF page. Just drop your handle and email in the [Google Sheet], and you're good to go!

https://docs.google.com/forms/d/e/1FAIpQLSdwSP5SG5KOWC9Wm2Hd7FoI4dguC1cxTz0W-9b302IqMlo-Gg/viewform?usp=dialog


## If you wanna use/ look at the code :
## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/codeforces-rating-bot.git
   ```
2. Navigate to the project directory:
   ```
   cd codeforces-rating-bot
   ```
3. (Optional) For local development, install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

This bot is designed to be run via GitHub Actions and uses Google Sheets as a database for users.

## Behind the Scenes Jargon

### 1. Google Sheet Setup

I have a google sheet that you can add your handle and account (where u want emails to be sent).

https://docs.google.com/forms/d/e/1FAIpQLSdwSP5SG5KOWC9Wm2Hd7FoI4dguC1cxTz0W-9b302IqMlo-Gg/viewform?usp=dialog


### 2. Google Cloud Platform Setup

To allow the bot to access your Google Sheet, you need to create a service account.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the "Google Drive API" and "Google Sheets API".
4.  Create a service account from "IAM & Admin" > "Service Accounts".
5.  Grant the service account the "Editor" role.
6.  Create a JSON key for the service account and download the file.

### 3. Share Google Sheet

Share your Google Sheet with the service account's email address (found in the JSON key file) and give it "Editor" permissions.

### 4. GitHub Secrets Setup

In your GitHub repository, go to "Settings" > "Secrets and variables" > "Actions" and add the following secrets:

*   `GCP_SA_KEY`: The entire content of your downloaded JSON service account key file.
*   `SENDER_EMAIL`: The email address for sending notifications.
*   `SMTP_PASSWORD`: The password for the sender's email account (an app-specific password is recommended).
*   `SMTP_SERVER`: The SMTP server for your email provider (e.g., `smtp.gmail.com`).
*   `SMTP_PORT`: The SMTP port (e.g., `587`).

## Usage

The bot is configured to run automatically every 15 minutes using GitHub Actions. You can also trigger it manually from the "Actions" tab in your GitHub repository.

For local testing, create `config.ini` and `service_account.json` files with the appropriate content.

## Success Metrics

The bot's success can be measured by:

*   Successful email notifications to users.
*   Accurate and timely updates of user data in the Google Sheet.
*   Proper logging of bot activities and errors for troubleshooting.
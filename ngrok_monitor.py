from dotenv import load_dotenv
import os
import re
import time
import requests
import smtplib
import http.client, urllib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

PUSHOVER_API=os.environ.get('PUSHOVER_API')
PUSHOVER_EMAIL=os.environ.get('PUSHOVER_EMAIL')
PUSHOVER_API_MESSAGE_EP=os.environ.get('PUSHOVER_API_MESSAGE_EP')
PUSHOVER_AUTH_TOKEN=os.environ.get('PUSHOVER_AUTH_TOKEN')
PUSHOVER_AUTH_USER=os.environ.get('PUSHOVER_AUTH_USER')
NGROK_LOG=os.environ.get('NGROK_LOG')
OL_EMAIL=os.environ.get('OL_EMAIL')
OL_PW=os.environ.get('OL_PW')
OL_SMTP=os.environ.get('OL_SMTP')
OL_SMTP_PORT=os.environ.get('OL_SMTP_PORT')

def parse_log_line(log_line):
    pattern = re.compile(
        r't=(?P<timestamp>[\d\-T:]+-[\d]+) '
        r'lvl=(?P<level>\w+) '
        r'msg="(?P<message>[^"]+)" '
        r'obj=(?P<object>\w+) '
        r'id=(?P<id>\w+) '
        r'l=(?P<local>[\d\.]+:\d+) '
        r'r=(?P<remote>[\d\.]+:\d+)'
    )
    match = pattern.match(log_line)
    if match:
        return match.groupdict()
    return None

def send_email(recipient_email, subject, body):
    msg = MIMEText(body, "plain")
    try:
        with smtplib.SMTP(OL_SMTP, OL_SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.set_debuglevel(True)
            server.login(OL_EMAIL,OL_PW)
            server.sendmail(OL_EMAIL, recipient_email, msg.as_string())
            print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

def send_pushover_notification(message):
    print("\n")
    print("send_pushover_notification...")
    print("\n")
    try: 
        conn = http.client.HTTPSConnection(PUSHOVER_API)
        conn.request("POST", PUSHOVER_API_MESSAGE_EP,
        urllib.parse.urlencode({
            "token": PUSHOVER_AUTH_TOKEN,
            "user": PUSHOVER_AUTH_USER,
            "title": "New Website Visit!",
            "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def follow_log_file(log_file_path):
    subject = "Testing e-mail"
    body = "Testing email body"
    
    with open(log_file_path, 'r') as file:
        # Move the cursor to the end of the file
        file.seek(0, 2)

        while True:
            # Read new lines
            line = file.readline()
            if not line:
                # If no new line is found, wait for a short period and try again
                time.sleep(0.1)
                continue

            # Print the new line to the console (or process it as needed)
            print(line, end='')
            parsed_data = parse_log_line(line)
            print("parsed_data: ", parsed_data)
            send_email(PUSHOVER_EMAIL, subject, f"Remote IP: {parsed_data['remote']}\nvisited at {parsed_data['timestamp']}")
            # send_pushover_notification(f"Remote IP: {parsed_data['remote']}\nvisited at {parsed_data['timestamp']}")
            time.sleep(30)


if __name__ == '__main__':
    follow_log_file(NGROK_LOG)


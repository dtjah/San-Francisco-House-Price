import smtplib
import requests
import os
from email.mime.text import MIMEText

def analyze_data(repo_url):
    # Get the latest data from the GitHub repository
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return "Error while retrieving data: {}".format(e)

    # Perform data analysis here
    result = "Data analysis successful."
    return result

def send_email(result):
    sender = os.environ.get('MAIL_USERNAME')
    recipient = 'dtjahjadi1@babson.edu'
    subject = 'Data Analysis Result'
    message = 'The result of the data analysis is as follows: \n\n' + result

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Get the sender password from the GitHub secrets
    sender_password = os.environ.get('MAIL_PASSWORD')
 
    try:
        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, sender_password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        return "Error while sending email: {}".format(e)

# URL of the GitHub repository
repo_url = 'https://github.com/dtjah/San-Francisco-House-Price.git'

# Check for new data
try:
    response = requests.get(repo_url + '/commits')
    response.raise_for_status()
    commits = response.json()
    new_data = len(commits) > 0 # Change this line to check for new data in your use case
except requests.exceptions.RequestException as e:
    print("Error while checking for new data: {}".format(e))
else:
    if new_data:
        result = analyze_data(repo_url + '/contents/data.json')
        send_email(result)

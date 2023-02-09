import smtplib
import requests
from email.mime.text import MIMEText

def analyze_data(repo_url):
    # Get the latest data from the GitHub repository
    response = requests.get(repo_url)
    data = response.json()

    # Perform data analysis here
    result = "Data analysis successful."
    return result

def send_email(result):
    sender = 'davidsetiawantjahjadi@gmail.com'
    recipient = 'dtjahjadi1@babson.edu'
    subject = 'Data Analysis Result'
    message = 'The result of the data analysis is as follows: \n\n' + result

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, 'sender_password')
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

# URL of the GitHub repository
repo_url = 'https://api.github.com/repos/user/repo'

# Check for new data
response = requests.get(repo_url + '/commits')
commits = response.json()
new_data = len(commits) > 0 # Change this line to check for new data in your use case
if new_data:
    result = analyze_data(repo_url + '/contents/data.json')
    send_email(result)

import os
import requests

def get_secret(secret_name):
    response = requests.get(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/actions/secrets/{secret_name}",
                            headers={"Authorization": f"token {os.environ['GITHUB_TOKEN']}"})
    if response.status_code == 200:
        return response.json()["encrypted_value"]
    else:
        raise Exception(f"Failed to retrieve secret {secret_name}: {response.json()['message']}")

def send_email(subject, message):
    email = get_secret("MAIL_USERNAME")
    password = get_secret("MAIL_PASSWORD")
    # Connect to the email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    # Construct the email message
    email_message = f"Subject: {subject}\n\n{message}"
    # Send the email
    server.sendmail(email, "dtjahjadi1@babson.edu", email_message)
    # Close the connection to the email server
    server.quit()

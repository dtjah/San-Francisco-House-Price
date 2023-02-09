import smtplib
import os
import requests

def get_email_and_password():
    email = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    return email, password

def send_email(subject, body, recipient):
    email, password = get_email_and_password()
    smtp_server = "smtp.gmail.com"
    port = 587
    
    message = f"Subject: {subject}\n\n{body}"
    
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(email, recipient, message)
    server.quit()

def main():
    repo_name = "San-Francisco-House-Price"
    url = f"https://api.github.com/repos/dtjah/{repo_name}/commits"
    response = requests.get(url)
    data = response.json()
    new_commit = data[0]["sha"]
    
    recipient = "dtjahjadi1@babson.edu"
    send_email("Github repository update", f"The repository {repo_name} has been updated with a new commit: {new_commit}", recipient)


if __name__ == "__main__":
    main()

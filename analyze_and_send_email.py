import smtplib
import os
import requests

def send_email(subject, body, recipient):
    email = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    if not email or not password:
        raise Exception("MAIL_USERNAME and MAIL_PASSWORD must be set as environment variables.")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)
    message = f"Subject: {subject}\n\n{body}"
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

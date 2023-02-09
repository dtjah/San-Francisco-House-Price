import os
import requests
import smtplib
import time

def get_secret(secret_name):
    response = requests.get(f"https://api.github.com/repos/dtjah/San-Francisco-House-Price/actions/secrets/{secret_name}",
                            headers={"Authorization": f"token {os.environ['GITHUB_TOKEN']}"})
    if response.status_code == 200:
        return response.json()["encrypted_value"]
    else:
        raise Exception(f"Failed to retrieve secret {secret_name}: {response.json()['message']}")

def get_latest_commit(repo_name):
    # Use the Github API to fetch information about the repository
    response = requests.get(f"https://api.github.com/repos/{repo_name}/commits")
    # Extract the latest commit hash from the response
    latest_commit = response.json()[0]["sha"]
    return latest_commit

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

def main():
    repo_name = "dtjah/San-Francisco-House-Price"
    # Get the latest commit for the first time
    latest_commit = get_latest_commit(repo_name)
    while True:
        # Check for changes every 60 seconds
        time.sleep(60)
        new_commit = get_latest_commit(repo_name)
        if new_commit != latest_commit:
            # A new commit has been pushed to the repository
            send_email("Github repository update", f"The repository {repo_name} has been updated with a new commit: {new_commit}")
            # Update the latest commit
            latest_commit = new_commit

if __name__ == "__main__":
    main()

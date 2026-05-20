from bs4 import BeautifulSoup
import smtplib
import requests
from dotenv import load_dotenv
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

load_dotenv()


now = datetime.datetime.now()


# Email placeholder
content = ""

def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ""
    cnt += "<b>HN Top Stories:</b>\n" + "<br>" + "-"*50 + "<br>"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    for i, tag in enumerate(soup.find_all('span', class_='titleline')):
        cnt += ((str(i+1) + " :: " + tag.text + "\n" + "<br>") if tag.text != 'More' else "")
    return cnt


def send_email(subject, body, to_email):
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")

    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, to_email]):
        raise RuntimeError("Missing required SMTP configuration or recipient email.")

    msg = MIMEMultipart()
    msg['From'] = f"Wabtech Team <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = None
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        print(f"✅ Email sent successfully to {to_email}")
    except smtplib.SMTPException as exc:
        print(f"❌ Error sending email: {exc}")
        raise
    except Exception as exc:
        print(f"❌ Unexpected error sending email: {exc}")
        raise
    finally:
        if server is not None:
            try:
                server.quit()
            except Exception:
                pass



email_content = extract_news("https://news.ycombinator.com/")
content += email_content
content += ("<br>-----------------------------<br>")
content += "<br><br>End of Message"

email_subject = f"Top News Stories from Hacker News [Automated Email] - {now.strftime('%Y-%m-%d %H:%M:%S')}"

# Send the email
send_email(email_subject, content, os.getenv("TO_EMAIL"))
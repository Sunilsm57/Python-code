import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "smsunil57@gmail.com"
EMAIL_PASSWORD = "dfst owcg rkce onag"


def send_registration_email(to_email: str, username: str):

    subject = "Welcome to Our Application"

    body = f"""
    Hello {username},

    Your account has been successfully created.

    You can now login to the application.

    Regards,
    Support Team
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
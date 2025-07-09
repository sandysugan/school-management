import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Your OTP for Password Reset"

    body = f"Hello,\n\nYour OTP is: {otp}\nIt expires in 5 minutes.\n\nRegards, Team"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

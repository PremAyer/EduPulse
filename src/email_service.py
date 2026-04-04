# src/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_otp_email(receiver_email, otp_code):
    """Sends a 6-digit OTP code to the user's email."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials missing in .env")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "EduPulse System - Password Recovery"

    # HTML Email Body for a professional look
    body = f"""
    <html>
        <body>
            <h2>EduPulse Password Recovery</h2>
            <p>We received a request to reset your password. Here is your Secure Recovery Token:</p>
            <h1 style="color: #007bff; letter-spacing: 5px;">{otp_code}</h1>
            <p>Please enter this code in the application to create a new password. If you did not request this, please ignore this email.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    
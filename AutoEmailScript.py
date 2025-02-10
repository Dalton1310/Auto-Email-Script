import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError

# Function to check if an email is valid
def is_valid_email(email):
    try:
        valid = validate_email(email, check_deliverability=False)  # Set to True to check DNS
        return True
    except EmailNotValidError as e:
        print(f"Invalid email: {e}")
        return False

# Enter the SMTP server of the email provider. a list of common SMTP servers can be 
# found here: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html
smtp_server = 'ENTER SERVER HERE' 

# Enter the email address and password of the sender email. The password
# should be an app password if two-factor authentication is enabled for Gmail.
sender_email = 'ENTER SENDER EMAIL HERE' 
sender_password = 'ENTER PASSWORD HERE'

# Enter the email address of the receiver
receiver_email = 'ENTER RECEIVER EMAIL HERE'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

# Enter the subject and body of the email
message['Subject'] = 'ENTER SUBJECT OF EMAIL HERE'
body = 'ENTER MESSAGE OF EMAIL HERE'

message.attach(MIMEText(body, 'plain'))

# Validate emails before proceeding
if not is_valid_email(sender_email) or not is_valid_email(receiver_email):
    print("Invalid sender or receiver email.")
    exit()

try:
    with smtplib.SMTP(smtp_server, 587, timeout=10) as server:
        server.starttls()  # Upgrade connection to secure TLS
        server.login(sender_email, sender_password)  # Login
        server.sendmail(sender_email, receiver_email, message.as_string())  # Send email
    print("Email sent successfully.")
except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Check your email and password.")
except smtplib.SMTPConnectError:
    print("Failed to connect to the SMTP server.")
except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
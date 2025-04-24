from google.colab import files
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re
import csv
from getpass import getpass
import time
import logging
import atexit
import signal
import sys

# Configure logging
logging.basicConfig(filename='email_resume_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables
sender_email = ""
sender_password = ""
attachment_paths = []
email_list_file = ""
email_list = []
auth_success = False

def cleanup_files():
    """Delete uploaded email list and attachment files."""
    global email_list_file, attachment_paths
    for file_path in [email_list_file] + attachment_paths:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
                logging.info(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
                logging.error(f"Error deleting {file_path}: {e}")

# Register cleanup on exit
atexit.register(cleanup_files)

# Handle keyboard interrupt (Ctrl+C)
def signal_handler(sig, frame):
    print("\nProgram interrupted. Cleaning up files...")
    logging.info("Program interrupted. Cleaning up files.")
    cleanup_files()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def upload_files():
    """Upload email list (.csv or .txt) and multiple attachments (.pdf, .docx, .doc, .txt, .jpg, .jpeg, .png)."""
    global email_list_file, email_list, attachment_paths
    print("Upload email list file (.csv or .txt, emails in first column for .csv or one per line for .txt):")
    uploaded = files.upload()
    
    # Check for valid email list file
    email_file = None
    for filename in uploaded.keys():
        if filename.lower().endswith(('.csv', '.txt')):
            email_file = filename
            break
    
    if not email_file:
        print("Error: No .csv or .txt file uploaded. Please upload a .csv or .txt file.")
        logging.error("No .csv or .txt file uploaded.")
        return False
    
    # Save email list file
    email_list_file = email_file
    with open(email_list_file, "wb") as f:
        f.write(uploaded[email_file])
    
    # Read email list
    email_list.clear()
    try:
        if email_list_file.lower().endswith('.csv'):
            with open(email_list_file, "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].strip():
                        email_list.append(row[0].strip())
        else:  # .txt
            with open(email_list_file, "r", encoding='utf-8') as file:
                email_list.extend([line.strip() for line in file if line.strip()])
        
        if not email_list:
            print(f"Error: No valid email IDs found in {email_list_file}.")
            logging.error(f"No valid email IDs found in {email_list_file}.")
            return False
        
        # Validate email formats
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        invalid_emails = [email for email in email_list if not email_pattern.match(email)]
        if invalid_emails:
            print(f"Error: Invalid email(s) found: {invalid_emails}")
            logging.error(f"Invalid email(s) found: {invalid_emails}")
            return False
    except Exception as e:
        print(f"Error reading email list from {email_list_file}: {e}")
        logging.error(f"Error reading email list from {email_list_file}: {e}")
        return False
    
    # Upload attachments
    print("Upload attachment files (.pdf, .docx, .doc, .txt, .jpg, .jpeg, .png). Press Enter when done:")
    attachment_paths.clear()
    while True:
        try:
            uploaded = files.upload()
            if not uploaded:  # User pressed Enter or canceled upload
                break
            for filename in uploaded.keys():
                if filename.lower().endswith(('.pdf', '.docx', '.doc', '.txt', '.jpg', '.jpeg', '.png')):
                    with open(filename, "wb") as f:
                        f.write(uploaded[filename])
                    attachment_paths.append(filename)
                else:
                    print(f"Error: Unsupported file type for {filename}. Supported types: .pdf, .docx, .doc, .txt, .jpg, .jpeg, .png")
                    logging.error(f"Unsupported file type for {filename}")
        except Exception as e:
            print(f"Error uploading attachments: {e}")
            logging.error(f"Error uploading attachments: {e}")
            break
    
    if not attachment_paths:
        print("Error: No valid attachments uploaded. Please upload at least one supported file.")
        logging.error("No valid attachments uploaded.")
        return False
    
    print("Files uploaded successfully.")
    logging.info(f"Uploaded files: {email_list_file}, {attachment_paths}")
    return True

def test_authentication():
    """Test email authentication with retry option."""
    global sender_email, sender_password, auth_success
    max_attempts = 3
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\nAuthentication attempt {attempt}/{max_attempts}")
        if not sender_email or not sender_password or not auth_success:
            sender_email = input("Enter your Gmail address (e.g., your_email@gmail.com, or press Enter to skip): ").strip()
            if not sender_email:
                confirm = input("No email entered. Exit authentication? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("Authentication skipped.")
                    logging.info("Authentication skipped by user.")
                    return False
                continue
            print("Note: If 2FA is enabled, use a 16-character app password (not your regular password).")
            print("Generate one at https://myaccount.google.com/security > Search 'app passwords' > Create with a custom name.")
            sender_password = getpass("Enter your Gmail app password (16-character code): ").strip()
            # Normalize password to remove non-ASCII characters (e.g., non-breaking spaces)
            sender_password = sender_password.replace('\xa0', ' ').encode('ascii', 'ignore').decode('ascii')
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.set_debuglevel(1)  # Enable debug output
            server.starttls()
            server.login(sender_email, sender_password)
            server.quit()
            print("Authentication successful!")
            logging.info(f"Authentication successful for {sender_email}.")
            auth_success = True
            return True
        except smtplib.SMTPAuthenticationError as e:
            print("Authentication failed. Possible issues:")
            print("- Incorrect email or app password.")
            print("- 2FA enabled without an app password (generate one at https://myaccount.google.com/security).")
            print("- Account may be locked or requires verification (check https://myaccount.google.com/security).")
            if "534-5.7.9" in str(e):
                print("- Specific error: Application-specific password required. Use a 16-character app password.")
            logging.error(f"Authentication failed for {sender_email}: {e}")
            if attempt < max_attempts:
                print("Please try re-entering credentials with a valid app password.")
            attempt += 1
        except smtplib.SMTPConnectError:
            print("Failed to connect to SMTP server. Check your internet connection.")
            logging.error("SMTPConnectError: Failed to connect to SMTP server.")
            return False
        except Exception as e:
            print(f"Unexpected error during authentication: {e}")
            logging.error(f"Unexpected error during authentication: {e}")
            return False
    
    print(f"Failed after {max_attempts} attempts. Please verify your Gmail settings at https://myaccount.google.com/security.")
    logging.error(f"Authentication failed after {max_attempts} attempts for {sender_email}.")
    return False

def send_email(recipient_email, subject, body, attachment_paths):
    """Send an email with multiple attachments to a single recipient."""
    global auth_success
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach body
    msg.attach(MIMEText(body, "plain"))

    # Attach files
    for file_path in attachment_paths:
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}"
            )
            msg.attach(part)
        except FileNotFoundError:
            print(f"Error: Attachment file '{file_path}' not found.")
            logging.error(f"Attachment file '{file_path}' not found.")
            return False

    # Send email with retry for temporary errors
    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            print(f"Email sent to {recipient_email}")
            logging.info(f"Email sent to {recipient_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            print("Authentication error. Please re-test authentication (Option 3).")
            logging.error(f"Authentication error for {recipient_email}: SMTPAuthenticationError")
            auth_success = False
            return False
        except smtplib.SMTPRecipientsRefused:
            print(f"Recipient {recipient_email} refused. Possible invalid email.")
            logging.error(f"Recipient {recipient_email} refused.")
            return False
        except smtplib.SMTPServerDisconnected:
            print(f"Server disconnected for {recipient_email}. Attempt {attempt}/{max_retries}.")
            logging.error(f"Server disconnected for {recipient_email}. Attempt {attempt}/{max_retries}.")
            if attempt == max_retries:
                print("Max retries reached. Skipping this email.")
                logging.error(f"Max retries reached for {recipient_email}.")
                return False
            time.sleep(5)  # Wait before retry
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            logging.error(f"Failed to send email to {recipient_email}: {e}")
            return False

def send_all_emails():
    """Send emails to all email IDs."""
    if not email_list:
        print("Error: No email list loaded. Please upload files first (Option 1).")
        logging.error("No email list loaded.")
        return
    if not auth_success:
        print("Error: Please test authentication first (Option 3).")
        logging.error("Authentication not tested.")
        return
    if not attachment_paths:
        print("Error: No attachments uploaded. Please upload files first (Option 1).")
        logging.error("No attachments uploaded.")
        return

    subject = input("Enter email subject (e.g., Application for Data Scientist - Your Name): ").strip()
    body = input("Enter email body (press Enter for default):\n").strip() or """
Dear Hiring Manager,

I hope this email finds you well. I am writing to apply for the [Job Role] position at your company. Please find my application materials attached for your review.

Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience align with your team's needs.

Best regards,
Your Name
"""

    success_count = 0
    for email in email_list:
        if send_email(email, subject, body, attachment_paths):
            success_count += 1
        time.sleep(2)  # Delay to avoid rate limits
    print(f"\nSummary: {success_count}/{len(email_list)} emails sent successfully.")
    logging.info(f"Summary: {success_count}/{len(email_list)} emails sent successfully.")

def view_uploaded_files():
    """Display uploaded email list and check attachments."""
    if os.path.exists(email_list_file):
        print(f"\nEmail List File ({email_list_file}):")
        with open(email_list_file, "r", encoding='utf-8') as file:
            print(file.read())
    else:
        print("No email list file found.")
        logging.info("No email list file found.")
    
    if attachment_paths:
        print("\nAttachment files:")
        for file_path in attachment_paths:
            if os.path.exists(file_path):
                print(f"- {file_path} (found)")
                logging.info(f"Attachment file: {file_path} (found)")
            else:
                print(f"- {file_path} (not found)")
                logging.info(f"Attachment file: {file_path} (not found)")
    else:
        print("No attachment files found.")
        logging.info("No attachment files found.")

def main_menu():
    """Display menu and handle user choices."""
    while True:
        print("\n=== Email Sender Menu ===")
        print("1. Upload email list (.csv or .txt) and attachments (.pdf, .docx, .doc, .txt, .jpg, .jpeg, .png)")
        print("2. Send emails to all recipients")
        print("3. Test email authentication")
        print("4. View uploaded files")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            upload_files()
        elif choice == "2":
            send_all_emails()
        elif choice == "3":
            test_authentication()
        elif choice == "4":
            view_uploaded_files()
        elif choice == "5":
            print("Exiting program.")
            logging.info("Program exited.")
            cleanup_files()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            logging.warning(f"Invalid menu choice: {choice}")

if __name__ == "__main__":
    main_menu()
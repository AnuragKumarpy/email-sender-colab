
# Email-Sender-Colab

## About The Project
Email-Sender-Colab is a Python script designed to send emails with multiple attachments to a list of recipients using a Gmail account in Google Colab. It’s ideal for job applications, marketing campaigns, or bulk emailing tasks. The script supports Gmail’s 2FA with app passwords, ensures security by deleting uploaded files on exit or cancellation, and logs all actions for transparency. With input validation and rate limit handling, it’s reliable for personal and professional use.

## Getting Started
To use the script, you’ll need a Gmail account with 2FA enabled, access to Google Colab, and prepared email list and attachment files. Follow the steps below to set up and run the script.

### Prerequisites
- **Gmail Account**: Must have 2FA enabled and a 16-character app password generated.
- **Google Colab**: Accessible at https://colab.research.google.com.
- **Files**:
  - Email list in `.csv` (emails in first column) or `.txt` (one email per line) format.
  - Attachments in `.pdf`, `.docx`, `.doc`, `.txt`, `.jpg`, `.jpeg`, or `.png` formats.
- **Internet Connection**: Required for Colab and Gmail SMTP communication.

### Installation
1. **Clone or Download the Repository**:
   - Clone using Git:
     ```bash
     git clone https://github.com/your-username/email-sender-colab.git
     ```
   - Or download `email_resume_colab.py` from the repository’s main page.

2. **Open Google Colab**:
   - Visit https://colab.research.google.com.
   - Create a new notebook or upload `email_resume_colab.py`.

3. **Prepare Files**:
   - See *Usage* section for details on creating email list and attachment files.

## Usage
Follow these steps to generate an app password, prepare files, and run the script.

### Generate a Gmail App Password
1. Log in to your Gmail account at https://mail.google.com.
2. Go to https://myaccount.google.com/security.
3. In the **search bar** at the top, type `app passwords` and press Enter.
4. Click **App passwords** (you may need to verify your identity with 2FA).
5. Select **Mail** as the app and **Other** as the device.
6. Enter a custom name (e.g., `Colab Email Sender`) and click **Generate**.
7. Copy the **16-character app password** (e.g., `abcd efgh ijkl mnop`, including spaces).
8. Save it securely (e.g., in a text editor) to paste when prompted by the script.

### Prepare Files
#### Email List File
- **`.txt` File (e.g., `emails.txt`)**:
  - One email per line:
    ```plaintext
    hr1@company.com
    hr2@company.com
    ```
  - Save with any name.

- **`.csv` File (e.g., `recipients.csv`)**:
  - Emails in the first column, with optional additional columns:
    ```csv
    hr1@company.com,Company A
    hr2@company.com,Company B
    ```
  - Save with any name.

#### Attachment Files
- Supported formats: `.pdf`, `.docx`, `.doc`, `.txt`, `.jpg`, `.jpeg`, `.png`.
- Examples: `resume.pdf`, `cover_letter.docx`, `portfolio.jpg`.
- Use any file names.

### Run the Script
1. In Google Colab, paste `email_resume_colab.py` into a code cell or upload the file.
2. Click the play button or press `Shift + Enter` to run.
3. Follow the interactive menu:

#### Menu Options
- **1. Upload Email List and Attachments**:
  - Upload a `.csv` or `.txt` email list.
  - Upload one or more attachments (`.pdf`, `.docx`, `.doc`, `.txt`, `.jpg`, `.jpeg`, `.png`).
  - Press Enter when done uploading attachments.
  - The script validates email formats and file types, showing errors for unsupported files (e.g., `.zip`).

- **2. Send Emails to All Recipients**:
  - Enter an email **subject** (e.g., `Application for Data Scientist - Your Name`).
  - Enter an email **body** or press Enter for the default:
    ```plaintext
    Dear Hiring Manager,

    I hope this email finds you well. I am writing to apply for the [Job Role] position at your company. Please find my application materials attached for your review.

    Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience align with your team's needs.

    Best regards,
    Your Name
    ```
  - Emails are sent to all recipients with attachments, with a 2-second delay to avoid Gmail’s rate limits.

- **3. Test Email Authentication**:
  - Enter your Gmail address (e.g., `your_email@gmail.com`).
  - Paste the 16-character app password.
  - Tests SMTP authentication and logs the result.
  - If you skip entering an email, type `y` to exit or `n` to retry.

- **4. View Uploaded Files**:
  - Displays email list content and attachment status (found or not found).

- **5. Exit**:
  - Exits the program and deletes all uploaded files (email list and attachments).

### Check Logs and Emails
- **Logs**: Download `email_resume_log.txt` from Colab’s `Files` tab (left sidebar) to review authentication, uploads, email sending, and file deletions.
- **Emails**: Check the “Sent” folder in your Gmail account to confirm emails were sent with attachments.

## Roadmap
- Add support for BCC or CC recipients.
- Implement customizable email templates.
- Support additional attachment types (e.g., `.zip`, `.xlsx`).
- Add progress bar for email sending.
- Integrate with other email providers (e.g., Outlook).

## Contributing
Contributions are welcome to improve the script! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make changes and commit: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request with a detailed description of your changes.

### Reporting Issues
- Open an issue in the repository with details of the bug or feature request.

## License
Distributed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or feedback, open an issue in the GitHub repository or contact the maintainer via GitHub.

- Project Link: https://github.com/your-username/email-sender-colab

## Acknowledgments
- **Python Community**: For libraries like `smtplib`, `email`, and `google.colab`.
- **Google Colab**: For providing a free cloud-based Python environment.
- **Gmail SMTP**: For reliable email sending capabilities.
- **Contributors**: Thanks to anyone who submits issues or pull requests to improve this project.

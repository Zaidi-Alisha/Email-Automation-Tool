# Email Automation Tool with Google Sheets Integration

## Overview
A professional, cloud-based email automation tool that integrates seamlessly with Google Sheets for bulk email sending. Designed for outreach, marketing, and business development, this tool provides real-time collaboration, advanced tracking, and professional email delivery.

---

## Key Features

- **Google Sheets Integration:**
  - Direct integration with Google Sheets - no file uploads needed
  - Real-time data access and collaboration
  - Automatic row removal after successful email sending
  - Support for custom worksheet names
  - Required columns: Lead Name, Email address, Status, Instagram Link, Followers, Category, Website

- **Multi-User Email Sending:**
  - Configure up to 8 email accounts simultaneously for parallel sending
  - Each user can specify their own email count (1-30 emails per user)
  - Automatic contact allocation: contacts are distributed sequentially among users
  - Real-time quota validation shows which users can send emails
  - Parallel processing significantly increases sending speed

- **Advanced Sender Management:**
  - Supports Gmail, Outlook, Yahoo, Hotmail, and custom SMTP providers
  - Individual authentication for each user account
  - Enforces a 24-hour cooldown per sender (tracked in `sender_usage.json`)
  - Each sender can send up to 30 emails per 24 hours
  - Real-time remaining quota display for each user after sending

- **Enhanced Email Sending:**
  - Multi-user parallel sending with automatic contact distribution
  - Customizable email subject and body with support for `[Lead Name]` placeholder
  - Supports file attachments (multiple files) for all users
  - Real-time progress tracking per user with detailed results
  - No duplicate sending: each recipient only receives one email
  - Comprehensive error handling with user-friendly messages

- **Advanced Email Tracking:**
  - **Three-Status System:** not viewed (default), viewed, replied
  - **Unique Tracking IDs:** Each email gets a unique tracking identifier
  - **Email Open Tracking:** 1x1 pixel GIF tracks when emails are opened
  - **Reply Tracking:** Optional endpoint to track email replies
  - **Real-time Status Updates:** Status updates automatically when emails are opened
  - **Tracking Server:** Dedicated Flask server for handling tracking requests

- **Follow-Up Email System:**
  - Send follow-up emails to recipients who haven't viewed their original emails
  - Customizable follow-up delay (up to 300 hours)
  - Support for attachments in follow-up emails
  - Background scheduler runs every 5 minutes
  - Targets only "not viewed" status recipients

- **Spam Prevention:**
  - "Check Spam Score" button scans your subject and body for common spam trigger words
  - Highlights risky words and provides a spam score and suggestions before sending
  - Helps you optimize your content for inbox delivery

- **Comprehensive Logging:**
  - Logs each sent email to `sent_log.csv` with tracking ID and status
  - Real-time status tracking (not viewed → viewed → replied)
  - Follow-up scheduling and execution logs
  - Tracks sender usage in `sender_usage.json` to enforce cooldown.

- **UI/UX:**
  - Modern, professional Streamlit web interface.
  - Progress bar, real-time status, and summary reporting.
  - User-friendly error messages and guidance.

---

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the app:**
   ```bash
   streamlit run app.py
   ```
2. **Multi-User Setup:**
   - In the sidebar, set the "Number of Users" (1-8).
   - For each user, configure:
     - Email address and password
     - Email provider (Gmail, Outlook, Yahoo, Hotmail, or Other)
     - Number of emails to send (1-30 per user)
     - Custom SMTP settings if using "Other" provider
   - The tool will show real-time validation and contact allocation.

3. **Sending Emails:**
   - Click "Send Emails to Clients" button.
   - Write or paste your email subject and body (use `[Fullname]` for personalization).
   - (Optional) Upload attachments that will be sent with all emails.
   - Click **"Check Spam Score"** to scan your content and get optimization suggestions.
   - Click **"Send Emails"** to start multi-user parallel sending.
   - Monitor real-time progress and detailed per-user results.
   - View remaining email quotas for each user after sending.

4. **Follow-Up Emails:**
   - Click "Send Follow-up Emails" button.
   - The tool shows recipients who haven't viewed their emails.
   - Write your follow-up subject and body (use `[Lead name]` for personalization).
   - (Optional) Upload attachments for follow-up emails.
   - Click **"Send Follow-Up Emails to Not Viewed"**.
   - Currently uses the first configured user (multi-user follow-up coming soon).

---

## Error Handling & Troubleshooting

The tool includes comprehensive error handling with user-friendly messages to help you quickly identify and resolve issues:

### **Common Issues and Solutions:**

**Contact File Issues:**
- "No contacts found. Please check your contacts.xlsx file." - Ensure contacts.xlsx exists in the project directory.
- "Your contacts file is missing these required columns..." - Add the missing columns to your Excel file.
- "Unable to read your contacts file..." - Check that your Excel file isn't corrupted or open in another program.

**User Configuration Issues:**
- "Please configure at least one user in the sidebar..." - Set up at least one email account in the sidebar.
- "User X has reached 24h limit" - Wait 24 hours or use a different email account.
- "Authentication failed" - Check your email and password. For Gmail, use an App Password.
- "Custom SMTP settings missing..." - Provide both host and port for custom email providers.

**Email Content Issues:**
- "Please enter an email subject..." - Add a subject line before sending.
- "Please enter an email message..." - Add email content before sending.
- "Email address 'X' is not valid" - Fix invalid email addresses in your contacts file.

**Network and Connection Issues:**
- "Failed to send to [email]" - Check your internet connection and email provider settings.
- "Timeout" errors - Try reducing the number of users or emails per batch.

### **Advanced Error Recovery:**
- The tool continues processing even if individual emails fail.
- Each user operates independently - one user's failure won't affect others.
- Detailed error logs help identify specific issues.
- Automatic retry mechanisms for temporary network issues.
- Safe file operations prevent data corruption.

---

## Best Practices for Inbox Delivery
- Avoid spammy words/phrases in your subject and body.
- Personalize your emails using the `[Lead name]` placeholder.
- Use reputable email providers (Gmail, Outlook, Yahoo, Hotmail).
- Do not send more than 30 emails per sender per 24 hours.
- Test with your own accounts to verify inbox placement.
- For custom domains, set up SPF/DKIM/DMARC in your DNS.
- Use multiple accounts to increase your daily sending capacity.

---

## File Descriptions
- `app.py` — Main Streamlit app.
- `requirements.txt` — Python dependencies.
- `contacts.xlsx` — Your contact list (input file).
- `sent_log.csv` — Log of all sent emails.
- `sender_usage.json` — Tracks sender cooldowns.
- `README.md` — This documentation.

---

**Copyright Notice**

This software and all related materials are the exclusive intellectual property of Alisha Zaidi. Unauthorized copying, redistribution, or marketing of this tool, in whole or in part, is strictly prohibited. You may not claim this tool as your own work or remove this notice from any distribution. All rights reserved.

© Alisha Zaidi. All rights reserved. 
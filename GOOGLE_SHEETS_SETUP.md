# Google Sheets Integration Setup Guide

## Overview
This email automation tool now supports Google Sheets instead of Excel files. This allows for real-time collaboration and easier access from anywhere.

## Required Google Sheets Structure
Google sheet columns:
- **Lead Name** - Name of the contact
- **Email address** - Email address to send to
- **Status** - Email status (not viewed/viewed/replied)
- **Instagram Link** - Instagram profile URL
- **Followers** - Number of followers
- **Category** - Contact category
- **Website** - Contact website
- **Email** - Additional email field (optional)

## Setup Instructions

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

### Step 2: Enable APIs
1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search and enable:
   - **Google Sheets API**
   - **Google Drive API**

### Step 3: Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Enter service account details:
   - Name: `email-automation-service`
   - Description: `Service account for email automation tool`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

### Step 4: Generate Credentials File
1. Click on the created service account
2. Go to the "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Select "JSON" format
5. Download the file
6. **Important**: Rename the downloaded file to `google_credentials.json`
7. Place it in your email automation tool folder

### Step 5: Share Your Google Sheet
1. Open your Google Sheet
2. Click the "Share" button (top right)
3. Add the service account email with "Editor" permissions
   - The email is found in the `client_email` field of your `google_credentials.json` file
   - It looks like: `email-automation-service@your-project.iam.gserviceaccount.com`
4. Click "Send"

### Step 6: Configure in the App
1. Run your email automation tool: `streamlit run app.py`
2. In the sidebar, expand "Google Sheets Setup"
3. Check "Use Google Sheets instead of Excel"
4. Paste your Google Sheets URL or ID
5. Click "Test Google Sheets Connection" to verify

## Status Tracking System

The tool now supports three email statuses:

1. **not viewed** (default) - Email sent but not opened
2. **viewed** - Email opened (tracked via pixel)
3. **replied** - Recipient replied to email

## Tracking Features

- **Email Open Tracking**: 1x1 pixel GIF tracks when emails are opened
- **Unique Tracking IDs**: Each email gets a unique tracking ID for accurate monitoring
- **Reply Tracking**: Optional reply tracking endpoint
- **Real-time Updates**: Status updates in real-time when emails are opened

## Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check that `google_credentials.json` is in the correct folder
   - Verify the service account email has access to your sheet

2. **"Sheet not found"**
   - Ensure the Google Sheets URL is correct
   - Check that the sheet is shared with the service account

3. **"Missing columns"**
   - Verify your sheet has all required columns
   - Column names are case-insensitive but must match exactly

4. **"No data found"**
   - Ensure your sheet has data rows (not just headers)
   - Check that the worksheet name is correct (if specified)

### Testing Connection:
Use the "Test Google Sheets Connection" button in the sidebar to verify your setup.

## Benefits of Google Sheets Integration

- ✅ Real-time collaboration
- ✅ Access from anywhere
- ✅ Automatic backups
- ✅ Version history
- ✅ Easy sharing with team members
- ✅ No file upload/download needed
- ✅ Automatic sync with email tool

## Security Notes

- Keep your `google_credentials.json` file secure
- Don't share it publicly or commit it to version control
- The service account only has access to sheets you explicitly share
- Consider using environment variables for production deployments

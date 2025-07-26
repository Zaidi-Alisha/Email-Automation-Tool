import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import os
import re

class GoogleSheetsManager:
    def __init__(self, credentials_file="google_credentials.json"):
        self.credentials_file = credentials_file
        self.gc = None
        self.setup_credentials()
    
    def setup_credentials(self):
        if os.path.exists(self.credentials_file):
            try:
                scope = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file(self.credentials_file, scopes=scope)
                self.gc = gspread.authorize(creds)
                return True
            except Exception as e:
                st.error(f"Error setting up Google Sheets credentials: {str(e)}")
                return False
        return False
    
    def extract_sheet_id(self, url_or_id):
        if url_or_id.startswith('http'):
            match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
            if match:
                return match.group(1)
            else:
                raise ValueError("Invalid Google Sheets URL format")
        else:
            return url_or_id
    
    def read_sheet_as_dataframe(self, sheet_url_or_id, worksheet_name=None):
        if not self.gc:
            raise Exception("Google Sheets not properly initialized. Check credentials.")
        
        try:
            sheet_id = self.extract_sheet_id(sheet_url_or_id)
            spreadsheet = self.gc.open_by_key(sheet_id)
            
            if worksheet_name:
                worksheet = spreadsheet.worksheet(worksheet_name)
            else:
                worksheet = spreadsheet.sheet1
            
            # Get all values to handle duplicate headers manually
            all_values = worksheet.get_all_values()
            if not all_values:
                return pd.DataFrame()
            
            # Get headers and handle duplicates
            headers = all_values[0]
            data_rows = all_values[1:]
            
            # Handle duplicate headers by adding suffixes
            seen_headers = {}
            clean_headers = []
            for header in headers:
                if header in seen_headers:
                    seen_headers[header] += 1
                    clean_headers.append(f"{header}_{seen_headers[header]}")
                else:
                    seen_headers[header] = 0
                    clean_headers.append(header)
            
            # Create DataFrame with clean headers
            df = pd.DataFrame(data_rows, columns=clean_headers)
            df = df.dropna(how='all')
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading Google Sheet: {str(e)}")
    
    def update_sheet_data(self, sheet_url_or_id, dataframe, worksheet_name=None):
        if not self.gc:
            raise Exception("Google Sheets not properly initialized. Check credentials.")
        
        try:
            sheet_id = self.extract_sheet_id(sheet_url_or_id)
            spreadsheet = self.gc.open_by_key(sheet_id)
            
            if worksheet_name:
                worksheet = spreadsheet.worksheet(worksheet_name)
            else:
                worksheet = spreadsheet.sheet1
            
            worksheet.clear()
            worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
            
        except Exception as e:
            raise Exception(f"Error updating Google Sheet: {str(e)}")
    
    def remove_rows_by_indices(self, sheet_url_or_id, indices_to_remove, worksheet_name=None):
        if not self.gc:
            raise Exception("Google Sheets not properly initialized. Check credentials.")
        
        try:
            df = self.read_sheet_as_dataframe(sheet_url_or_id, worksheet_name)
            df_updated = df.drop(indices_to_remove).reset_index(drop=True)
            self.update_sheet_data(sheet_url_or_id, df_updated, worksheet_name)
            
        except Exception as e:
            raise Exception(f"Error removing rows from Google Sheet: {str(e)}")
    
    def test_connection(self, sheet_url_or_id):
        try:
            df = self.read_sheet_as_dataframe(sheet_url_or_id)
            return True, f"Successfully connected! Found {len(df)} rows of data."
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

    def validate_required_columns(self, sheet_url_or_id, worksheet_name=None):
        """
        Validates that the sheet contains all required columns (case-insensitive).
        Raises an Exception with a user-friendly message if any are missing.
        """
        required_columns = [
            "Lead Name",
            "Email Address",
            "Status",
            "Instagram Link",
            "Followers",
            "Category",
            "Website",
            "Email"
        ]
        df = self.read_sheet_as_dataframe(sheet_url_or_id, worksheet_name)
        df_columns_lower = [col.lower() for col in df.columns]
        missing = [col for col in required_columns if col.lower() not in df_columns_lower]
        if missing:
            raise Exception(f"The following required columns are missing from the sheet: {', '.join(missing)}. Please update your Google Sheet to include all required columns.")
        return True

def create_credentials_instructions():
    """
    Display instructions for setting up Google Sheets API credentials
    """
    st.markdown("""
    ### Setting up Google Sheets Integration
    
    To use Google Sheets instead of Excel, you need to set up Google Sheets API credentials:
    
    #### Step 1: Create a Google Cloud Project
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
    2. Create a new project or select an existing one
    
    #### Step 2: Enable Google Sheets API
    1. In the Google Cloud Console, go to "APIs & Services" > "Library"
    2. Search for "Google Sheets API" and enable it
    3. Also enable "Google Drive API"
    
    #### Step 3: Create Service Account
    1. Go to "APIs & Services" > "Credentials"
    2. Click "Create Credentials" > "Service Account"
    3. Fill in the details and create the service account
    
    #### Step 4: Generate Key File
    1. Click on the created service account
    2. Go to "Keys" tab
    3. Click "Add Key" > "Create New Key" > "JSON"
    4. Download the JSON file and save it as `google_credentials.json` in your project folder
    
    #### Step 5: Share Your Google Sheet
    1. Open your Google Sheet
    2. Click "Share" button
    3. Add the service account email (found in the JSON file) with "Editor" permissions
    
    #### Required Columns in Your Google Sheet:
    - Lead Name
    - Email Address
    - Status
    - Instagram Link
    - Followers
    - Category
    - Website
    - Email
    """)

def google_sheets_ui():
    st.sidebar.header("Google Sheets Integration")
    sheet_url_or_id = st.sidebar.text_input("Google Sheet URL or ID", key="sheet_url_or_id")
    worksheet_name = st.sidebar.text_input("Worksheet Name (optional)", key="worksheet_name")
    gs_manager = GoogleSheetsManager()
    sheet_status = st.sidebar.empty()
    if st.sidebar.button("Test Google Sheets Connection & Validate Columns"):
        try:
            ok, msg = gs_manager.test_connection(sheet_url_or_id)
            if not ok:
                sheet_status.error(msg)
                st.session_state['sheet_validated'] = False
                return None, None
            gs_manager.validate_required_columns(sheet_url_or_id, worksheet_name)
            sheet_status.success("Google Sheet is valid and all required columns are present!")
            st.session_state['sheet_validated'] = True
            st.session_state['validated_sheet_url_or_id'] = sheet_url_or_id
            st.session_state['validated_worksheet_name'] = worksheet_name
        except Exception as e:
            sheet_status.error(str(e))
            st.session_state['sheet_validated'] = False
            return None, None
    # If already validated, return values
    if st.session_state.get('sheet_validated'):
        return st.session_state.get('validated_sheet_url_or_id'), st.session_state.get('validated_worksheet_name')
    return None, None

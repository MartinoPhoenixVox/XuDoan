import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def get_google_sheet(sheet_url):
    try:
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds_file = os.getenv('GOOGLE_CREDS_JSON', 'credentials.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        return client.open_by_url(sheet_url).sheet1
    except Exception as e:
        raise RuntimeError(f"Lỗi kết nối Google Sheets: {str(e)}")

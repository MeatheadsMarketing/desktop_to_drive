import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from pathlib import Path
import mimetypes
from datetime import datetime
import json

st.title("📤 Local Folder → Google Drive Uploader")

@st.cache_resource(show_spinner=False)
def get_drive_service():
    try:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gdrive_service_account"],
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        return build("drive", "v3", credentials=creds)
    except KeyError:
        st.error("""
        ❌ **Google Drive credentials not found!**
        
        To fix this, you need to:
        
        1. **Get Google Drive API credentials:**
           - Go to [Google Cloud Console](https://console.cloud.google.com/)
           - Create a new project or select existing one
           - Enable the Google Drive API
           - Create a Service Account
           - Download the JSON key file
        
        2. **For local development:**
           - Copy the JSON content to `.streamlit/secrets.toml` under `gdrive_service_account`
           - Or set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
        
        3. **For Streamlit Cloud:**
           - Go to your app settings
           - Add the JSON content as a secret named `gdrive_service_account`
        
        See the README.md for detailed setup instructions.
        """)
        return None
    except Exception as e:
        st.error(f"❌ Error setting up Google Drive service: {str(e)}")
        return None

drive_service = get_drive_service()

def ensure_drive_folder(name):
    results = drive_service.files().list(q=f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                                         fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]

def upload_file(local_path, drive_folder_id):
    file_name = os.path.basename(local_path)
    mime_type, _ = mimetypes.guess_type(local_path)
    file_metadata = {"name": file_name, "parents": [drive_folder_id]}
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    uploaded = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return uploaded.get("id")

local_folder = st.text_input("Enter path to local folder (e.g. ~/Desktop/staging/threads_export):").strip()
drive_folder_name = st.text_input("Enter Google Drive destination folder (e.g. gpt_threads):").strip()

if local_folder and drive_folder_name and st.button("🚀 Upload to Drive"):
    if drive_service is None:
        st.error("Cannot upload: Google Drive service not configured. Please set up credentials first.")
    else:
        local_folder = os.path.expanduser(local_folder)
        if not os.path.isdir(local_folder):
            st.error("Invalid folder path.")
        else:
            with st.spinner("Uploading..."):
                drive_folder_id = ensure_drive_folder(drive_folder_name)
                upload_log = []
                for root, _, files in os.walk(local_folder):
                    for f in files:
                        full_path = os.path.join(root, f)
                        try:
                            file_id = upload_file(full_path, drive_folder_id)
                            upload_log.append({
                                "name": f,
                                "local_path": full_path,
                                "status": "Success",
                                "file_id": file_id,
                                "timestamp": datetime.now().isoformat()
                            })
                        except Exception as e:
                            upload_log.append({
                                "name": f,
                                "local_path": full_path,
                                "status": f"Error: {e}",
                                "file_id": None,
                                "timestamp": datetime.now().isoformat()
                            })

                st.success(f"Uploaded {len([x for x in upload_log if x['status'] == 'Success'])} files")
                st.json(upload_log)
                with open("upload_log.jsonl", "w") as f:
                    for entry in upload_log:
                        f.write(json.dumps(entry) + "\n")

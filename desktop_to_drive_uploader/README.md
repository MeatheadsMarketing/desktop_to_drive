# Desktop to Drive Uploader

A Streamlit application that uploads all files from a local folder to Google Drive. Perfect for uploading exported ChatGPT threads or any other local files to Google Drive.

## Features

- 📁 Recursive folder upload (includes all subfolders)
- 🆕 Auto-create destination folder in Google Drive
- 📊 Upload progress tracking and logging
- 🔄 Retry support for failed uploads
- 🎯 Simple drag-and-drop or folder pick interface
- 📝 Detailed upload logs saved to JSONL format

## Setup Instructions

### 1. Google Cloud Console Setup

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Google Drive API:**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click on it and press "Enable"

3. **Create Service Account:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"

4. **Generate JSON Key:**
   - Click on your newly created service account
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Download the JSON file

5. **Share Google Drive Folder (Optional):**
   - If you want to upload to a specific folder, share it with your service account email
   - The service account email looks like: `your-service-account@your-project-id.iam.gserviceaccount.com`

### 2. Local Development Setup

1. **Install Dependencies:**
   ```bash
   pip install streamlit google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

2. **Configure Secrets:**
   
   **Option A: Using .streamlit/secrets.toml (Recommended)**
   - Create a `.streamlit` folder in your project directory
   - Create a `secrets.toml` file inside it
   - Copy the contents of your downloaded JSON key file into the `gdrive_service_account` field:
   
   ```toml
   gdrive_service_account = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-private-key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
     "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
     "client_id": "your-client-id",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
   }
   '''
   ```
   
   **Option B: Using Environment Variable**
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your JSON key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

3. **Run the Application:**
   ```bash
   streamlit run cockpit.streamlit.py
   ```

### 3. Streamlit Cloud Deployment

1. **Push to GitHub:**
   - Create a GitHub repository
   - Push your code to the repository

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Deploy the app

3. **Configure Secrets:**
   - In your Streamlit Cloud app settings
   - Go to "Secrets" section
   - Add the JSON content from your service account key file
   - Use the key name: `gdrive_service_account`

## Usage

1. **Enter Local Folder Path:**
   - Provide the full path to the folder you want to upload
   - Example: `~/Desktop/chatgpt_exports` or `/Users/username/Documents/threads`

2. **Enter Drive Folder Name:**
   - Specify the name of the destination folder in Google Drive
   - Example: `gpt_threads` or `my_exports`

3. **Upload:**
   - Click the "🚀 Upload to Drive" button
   - The app will create the destination folder if it doesn't exist
   - All files and subfolders will be uploaded recursively

## File Structure

```
desktop_to_drive_uploader/
├── cockpit.streamlit.py      # Main Streamlit application
├── .streamlit/
│   └── secrets.toml         # Local secrets configuration
├── README.md                # This file
└── upload_log.jsonl         # Generated upload logs
```

## Troubleshooting

### Common Issues

1. **"Google Drive credentials not found"**
   - Make sure you've configured the secrets properly
   - Check that the JSON key file is valid
   - Verify the service account has the necessary permissions

2. **"Invalid folder path"**
   - Ensure the local folder path exists
   - Use absolute paths or expand user paths (e.g., `~/Desktop`)

3. **"Permission denied" errors**
   - Make sure your service account has access to the Google Drive folder
   - Share the destination folder with your service account email

4. **Upload failures**
   - Check the upload log for specific error messages
   - Ensure files aren't too large (Google Drive has file size limits)
   - Verify your internet connection

### Getting Help

- Check the upload logs in `upload_log.jsonl` for detailed error information
- Ensure all dependencies are installed correctly
- Verify your Google Cloud project has billing enabled (required for API usage)

## Security Notes

- Never commit your service account JSON key to version control
- Use `.gitignore` to exclude sensitive files
- Regularly rotate your service account keys
- Grant minimal necessary permissions to your service account

## License

This project is open source and available under the MIT License. 
# Final Deployment Checklist

Follow these exact steps manually to complete the public deployment without compromising data.

## Google Cloud & Sheets Setup
- [ ] Create a new Google Sheet
- [ ] Rename the bottom worksheet tab to exactly `Sheet1`
- [ ] Copy the required headers from `10_Metadata/google_sheets_setup.md` into Row 1
- [ ] Create a Google Cloud Project
- [ ] Enable the Google Sheets API
- [ ] Enable the Google Drive API
- [ ] Create a Service Account
- [ ] Download the JSON key file for the Service Account
- [ ] Share the Google Sheet with the Service Account's `client_email` (give it "Editor" permissions)

## Streamlit Cloud Secrets Configuration
- [ ] Open `.streamlit/secrets.toml.example` and prepare your real secret format (DO NOT save real secrets in the project folder)
- [ ] Go to [share.streamlit.io](https://share.streamlit.io/)
- [ ] Click "New app" -> "Deploy a public app from GitHub"
- [ ] Select your Repository, Branch (`main`), and Main file path (`app.py`)
- [ ] Click "Advanced settings..."
- [ ] Paste your configured TOML secrets into the Secrets text box

## GitHub & Deployment Execution
- [ ] Create an empty public repository on your GitHub account
- [ ] Push this local codebase to your new GitHub repository
- [ ] Click "Deploy!" on Streamlit Community Cloud
- [ ] Wait for the app to finish building and booting up

## Live Testing
- [ ] Open the live public URL
- [ ] Verify that the fallback CSV warning is NO LONGER visible (this proves secrets are loaded correctly)
- [ ] Submit one real test evaluation (using your own email, do not use fake data)
- [ ] Verify the new row appears instantly in your private Google Sheet
- [ ] Attempt to submit a second evaluation with the exact same email to verify duplicate prevention works
- [ ] Switch to the Admin Dashboard and verify your test rating is calculated correctly

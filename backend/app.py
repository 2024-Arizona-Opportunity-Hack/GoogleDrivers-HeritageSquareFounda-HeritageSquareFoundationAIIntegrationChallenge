from flask import Flask, redirect, url_for, session, request, jsonify
from dotenv import load_dotenv
import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv('CLIENT_SECRET') 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'client_secrets.json'

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    # redirect_uri="http://localhost:5000/callback",
    redirect_uri="http://localhost:5000/callback"

)

# Helper function to get Google Drive API service
def get_gdrive_service():
    creds = None
    if 'credentials' in session:
        creds = pickle.loads(session['credentials'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
            session['credentials'] = pickle.dumps(creds)  # Save refreshed creds
        else:
            return None

    service = build('drive', 'v3', credentials=creds)
    return service

# API: Initiate Google OAuth login
@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

# API: OAuth callback to get user credentials
@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session['credentials'] = pickle.dumps(creds)
    return redirect(url_for('list_files'))

@app.route('/files', methods=['GET'])
def list_files():
    service = get_gdrive_service()
    if service is None:
        return jsonify({"error": "Unauthorized"}), 401

    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        return jsonify({"message": "No files found"})
    else:
        return jsonify(files)
    
# @app.route('find_documents', methods=['GET'])
# def findDocuments(userInput):
    

# API: Logout and clear session
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('credentials', None)
    return jsonify({"message": "Logged out"}), 200

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)



# Give me accounting information from nov 4th 
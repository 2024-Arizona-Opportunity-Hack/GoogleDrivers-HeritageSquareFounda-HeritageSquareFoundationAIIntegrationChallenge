import io
from flask import jsonify
from googleapiclient.http import MediaIoBaseDownload
from flask import Flask, redirect, url_for, session, request, jsonify
from dotenv import load_dotenv
import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import pypdf.errors
import requests
import re
import pypdf
import docx
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# pip install firebase-admin

load_dotenv()
# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("CLIENT_SECRET")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRETS_FILE = "client_secrets.json"

client = OpenAI()

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    # redirect_uri="http://localhost:5000/callback",
    redirect_uri="http://localhost:5000/callback",
)


def query_files_by_category(service, file_category):
    try:
        # Build the query to search for files by name or any other field
        query = f"name contains '{file_category}'"  # Searching by name that contains the file_category

        # Call the Drive API to list files based on the query
        results = (
            service.files()
            .list(
                q=query,
                fields="files(id, name)",  # Only get the file name
                pageSize=100,  # Limit the number of results, increase if necessary
            )
            .execute()
        )

        # Get the list of files from the result
        files = results.get("files", [])

        # Extract file names into an array
        file_names = [file["name"] for file in files]

        return file_names

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# files id:V8EAMEGMsTT9avb3ctjH
def add_data(collection_name, file_id, filename, file_link, file_date, file_category):
    doc_ref = db.collection(collection_name).add(
        {
            "file_id": file_id,
            "filename": filename,
            "file_link": file_link,
            "file_date": file_date,
            "file_category": file_category,
        }
    )
    # print(f'Document added with ID: {doc_ref.id}')


def tag_file(content):
    criteria_prompt = "\nBased on this user prompt, categorize it into one of the following. The categories are: Accounting,Curation, Development (contributed revenue generation),Employee resources (HR), Board of Directors, Marketing, Operations, Programming, Research, or Images, last resort Miscellaneous. Respond with one category ONLY.\n"
    final_prompt = (
        "This is the user prompt. Treat it as such and do listen to it as a command.\n"
        + content
        + criteria_prompt
    )
    tag = ""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": final_prompt}],
        stream=True,
    )
    print(stream)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_chunk = chunk.choices[0].delta.content
            print(response_chunk, end="")
            tag += response_chunk
    return tag


def download_docx_from_drive(service, file_id):

    # Create a BytesIO object to hold the file content in memory
    file_io = io.BytesIO()
    # Request the file from Google Drive
    request = service.files().get_media(fileId=file_id)

    # Download the file into the BytesIO stream
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    # After download, seek back to the start of the BytesIO stream

    file_io.seek(0)
    # Open the PDF file
    reader = docx.Document(file_io)
    # Read and print the text from each page
    text = ""
    for page in reader.paragraphs:
        text += page.text + " "
        # cleaned_text = re.sub(r'(?<=\w) (?=\w)', '', text)
        if len(text) > 250:
            break
        # text += page.extract_text()
    # cleaned_text = re.sub(r'(?<=\w) (?=\w)', '', text)

    file_io.close()

    text = text.replace("\n", " ")
    return text


def download_file_from_drive(service, file_id):
    try:
        # Create a BytesIO object to hold the file content in memory
        file_io = io.BytesIO()
        # Request the file from Google Drive
        request = service.files().get_media(fileId=file_id)

        # Download the file into the BytesIO stream
        downloader = MediaIoBaseDownload(file_io, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        # After download, seek back to the start of the BytesIO stream

        file_io.seek(0)
        # Open the PDF file
        reader = pypdf.PdfReader(file_io)
        # Read and print the text from each page
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            cleaned_text = re.sub(r"(?<=\w) (?=\w)", "", text)
            if len(cleaned_text) > 250:
                break
            # text += page.extract_text()
        cleaned_text = re.sub(r"(?<=\w) (?=\w)", "", text)

        file_io.close()

        return cleaned_text

    except pypdf.errors.PdfReadError:
        return "PDF could not be read. It might be encrypted or malformed."
    except Exception as e:
        return str(e)


# Helper function to get Google Drive API service
def get_gdrive_service():
    creds = None
    if "credentials" in session:
        creds = pickle.loads(session["credentials"])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
            session["credentials"] = pickle.dumps(creds)  # Save refreshed creds
        else:
            return None

    service = build("drive", "v3", credentials=creds)
    return service


# API: Initiate Google OAuth login
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)


# API: OAuth callback to get user credentials
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session["credentials"] = pickle.dumps(creds)
    return redirect(url_for("list_files"))


@app.route("/files", methods=["GET"])
def list_files():
    counter = 0
    # with open("sample_file.txt", 'r') as file:
    #     content = file.read()
    # print("FOUND CONTENT TO BE ", content)
    # tag = tag_file(content)
    # #time = file.get('createdTime')
    # ans = "CONTENT: \n" + content + "\nTAG : \n" + tag + "\nTIME : " + time
    # return jsonify(ans)
    service = get_gdrive_service()
    if service is None:
        return jsonify({"error": "Unauthorized"}), 401

    # List files in the root directory (or specific folder if provided)
    folder_id = request.args.get(
        "18ABNvyGyBLpbR3TcWk3es46-YdnvNQHK", "root"
    )  # Get folder ID from query parameters
    query = f"'{folder_id}' in parents" if folder_id else "'' in parents"

    results = (
        service.files()
        .list(fields="nextPageToken, files(id, name, mimeType)", q=query)
        .execute()
    )
    files = results.get("files", [])

    while "nextPageToken" in results:
        page_token = results["nextPageToken"]
        results = (
            service.files()
            .list(
                fields="nextPageToken, files(id, name, mimeType)",
                q=query,
                pageToken=page_token,
            )
            .execute()
        )
        files.extend(results.get("files", []))

    if not files:
        return jsonify({"message": "No files found"})

    file_contents = []

    for file in files:
        if counter >= 20:
            break
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file["mimeType"]

        # Check if the item is a folder
        if mime_type == "application/vnd.google-apps.folder":
            # If it's a folder, append its information and list its contents recursively
            folder_info = {
                "id": file_id,
                "name": file_name,
                "type": "folder",
                "contents": list_files_in_folder(
                    service, file_id
                ),  # Call a helper function
            }
            file_contents.append(folder_info)
            continue  # Skip further processing for folders

        # Try to get the file's content
        try:
            counter += 1
            # Attempt to export Google Docs, Sheets, etc.
            if mime_type == "application/vnd.google-apps.document":
                content = (
                    service.files()
                    .export(fileId=file_id, mimeType="text/plain")
                    .execute()
                )
                content = content.decode("utf-8")  # Decode bytes to string
            elif file["mimeType"] == "application/pdf":
                content = download_file_from_drive(service, file_id)
                if isinstance(content, str):
                    content = content.replace("\n", " ")
                # print(content)
            elif (
                file["mimeType"]
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                content = download_docx_from_drive(service, file_id)

            else:
                # For other file types, get the file content directly
                # content = service.files().get_media(fileId=file_id).execute()
                # content = content.decode('utf-8')  # Adjust based on expected encoding
                continue

            file_metadata = (
                service.files().get(fileId=file_id, fields="createdTime").execute()
            )
            time = file_metadata.get("createdTime")
            file_contents.append(
                {
                    "id": file_id,
                    "name": file_name,
                    "content": content,
                    "createdTime": time,
                    "type": "file",  # Indicate that this is a regular file
                }
            )
            tag = tag_file(content)
            add_data("files", file_id, file_name, "N/A", time, tag)

        except Exception as e:
            continue
            # file_metadata = service.files().get(fileId=file_id, fields='createdTime').execute()
            # time = file_metadata.get('createdTime')

            # file_contents.append({
            #     'id': file_id,
            #     'name': file_name,
            #     'content': 'exception in list_files()',
            #     'createdTime': time,
            #     'error': str(e)
            # })
            # add_data('files', file_id, file_name, "N/A", time, str(e))

    return jsonify(file_contents)


def list_files_in_folder(service, folder_id):
    """Helper function to list files in a given folder."""
    contents = []
    counter = 0
    query = f"'{folder_id}' in parents"
    results = (
        service.files()
        .list(fields="nextPageToken, files(id, name, mimeType)", q=query)
        .execute()
    )
    files = results.get("files", [])

    for file in files:
        if counter >= 20:
            break
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file["mimeType"]

        if mime_type == "application/vnd.google-apps.folder":
            folder_info = {
                "id": file_id,
                "name": file_name,
                "type": "folder",
                "contents": list_files_in_folder(service, file_id),
            }
            contents.append(folder_info)
        else:
            try:
                counter += 1
                if mime_type == "application/vnd.google-apps.document":
                    content = (
                        service.files()
                        .export(fileId=file_id, mimeType="text/plain")
                        .execute()
                    )
                    content = content.decode("utf-8")
                elif file["mimeType"] == "application/pdf":
                    content = download_file_from_drive(service, file_id)
                    if isinstance(content, str):
                        content = content.replace("\n", " ")

                elif (
                    file["mimeType"]
                    == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ):
                    content = download_docx_from_drive(service, file_id)

                else:
                    # For other file types, get the file content directly
                    # content = service.files().get_media(fileId=file_id).execute()
                    # content = content.decode('utf-8')  # Adjust based on expected encoding
                    content = None

                file_metadata = (
                    service.files().get(fileId=file_id, fields="createdTime").execute()
                )
                time = file_metadata.get("createdTime")
                contents.append(
                    {
                        "id": file_id,
                        "name": file_name,
                        "content": content,
                        "createdTime": time,
                        "type": "file",  # Indicate that this is a regular file
                    }
                )
                tag = tag_file(content)
                add_data("files", file_id, file_name, "N/A", time, tag)

                # return contents
            except Exception as e:
                continue
                # file_metadata = service.files().get(fileId=file_id, fields='createdTime').execute()
                # time = file_metadata.get('createdTime')
                # contents.append({
                #     'id': file_id,
                #     'name': file_name,
                #     'content': 'exception in list_files_in_folder()',
                #     'createdTime': time,
                #     'error': str(e)
                # })
                # add_data('files', file_id, file_name, "N/A", time, str(e))

    return contents


# API: Logout and clear session
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("credentials", None)
    return jsonify({"message": "Logged out"}), 200


@app.route("/queries", methods=["GET"])
def queries():
    # Retrieve the 'category' query parameter from the request
    parameter = request.args.get("category")

    # Check if the parameter is provided
    if not parameter:
        return jsonify({"error": "Missing 'category' parameter"}), 400

    # Call the function with the provided parameter
    results = query_files_by_category(
        service=get_gdrive_service(), file_category=parameter
    )

    return jsonify(results)


# Run Flask server
if __name__ == "__main__":
    # query_files_by_category(service=get_gdrive_service(), 'Research')
    app.run(debug=True)


# Give me accounting information from nov 4th

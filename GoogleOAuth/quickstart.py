import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GoogleDocsClient:
    def __init__(self, creds_path='./credentials.json', token_path='./token.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        self.creds_path = creds_path
        self.token_path = token_path
        self.creds = self.authenticate()
        self.service = self.build_docs_service()

    def authenticate(self):
        creds = None

        # Load token if available
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)

        # If no valid credentials, initiate OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token
            with open(self.token_path, 'w') as token_file:
                token_file.write(creds.to_json())

        return creds

    def build_docs_service(self):
        return build('docs', 'v1', credentials=self.creds)

    def create_document(self, title):
        doc = self.service.documents().create(body={'title': title}).execute()
        print(f"[+] Document created: {title} (ID: {doc.get('documentId')})")
        return doc.get('documentId')

    def insert_text(self, document_id, text):
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': text
            }
        }]
        self.service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        print(f"[+] Text inserted into document: {document_id}")


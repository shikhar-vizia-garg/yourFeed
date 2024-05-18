from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import os.path
import email

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate():
    """Authenticate the user and obtain credentials."""
    # Create flow instance without loading stored credentials
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    # Run the OAuth flow
    creds = flow.run_local_server(port=0)

    return creds


def read_emails(creds):
    """Read emails from the user's Gmail account."""
    # Import the Gmail API service
    from googleapiclient.discovery import build

    # Create the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    sender_email = "theodore@whiteboardcrypto.com"
    search_query = f"from:{sender_email}"
    # Call the Gmail API to retrieve the user's emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX'],q=search_query).execute()
    messages = results.get('messages', [])
    body = ''
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            message_parts = []
            for header in headers:
                if header['name'] == 'Subject':
                    print('Subject:', header['value'])
                elif header['name'] == 'From':
                    print('From:', header['value'])

            # If the email has multiple parts, loop through them and find the body
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        # print('Body:', body)
            else:
                # If the email has no parts, it means it's just plain text
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
                # print('Body:', body)

            print('-' * 50)

def read_emails_test(creds,sender_email):
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=creds)

    search_query = f"from:{sender_email}"
    results = service.users().messages().list(userId='me', labelIds=['INBOX'],q=search_query).execute()
    messages = results.get('messages', [])
    body = ''
    if not messages:
       return body
    else:
        message = messages[0]
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']
        message_parts = []
        for header in headers:
            if header['name'] == 'Subject':
                i = 0
                # print('Subject:', header['value'])
            elif header['name'] == 'From':
                i = 0
                # print('From:', header['value'])

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    # print('Body:', body)
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            # print('Body:', body)
    return body

def main():
    """Main function to authenticate and read emails."""
    creds = authenticate()
    # read_emails(creds)
    body = read_emails_test(creds)


if __name__ == '__main__':
    main()

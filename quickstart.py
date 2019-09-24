from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import urllib.error
import urllib.request as urllib2
import base64
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify']
import os


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    work_dir = os.getcwd()
    cert_dir = '%s/%s' % (work_dir, 'cert')
    cert_file = '%s/%s' % (cert_dir, 'cw-gmail-oauth-credential.json')
    token_file = '%s/%s' % (cert_dir, 'token.pickle')

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cert_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)


    results = service.users().getProfile(userId='me').execute()
    print(results)
    results = service.users().messages().list(userId='me').execute()
    if not results:
        print("No mails found.")
    else:
        print("Emails:")
        # https://developers.google.com/gmail/api/v1/reference/users/messages#resource
        for email in results['messages'][0:100]:
            email_message = GetMessage(service, 'me', email['id'])
            print(email['id'])
            message_id = email['id']
            for item in email_message['payload']['headers']:
                # print(item)
                if item['name'] == 'Subject':
                    subject = item.get('value')
                elif item['name'] == 'From':
                    From = item.get('value')

            # attachments_id = []
            print(subject, From)
            if 'parts' in email_message['payload']:
                for item in email_message['payload']['parts']:
                    if item['filename']:
                        print(item['filename'])
                        print(item['body']['attachmentId'])
                        attachments_id = item['body']['attachmentId']
                        GetAttachments(service, 'me', attachments_id, message_id, item['filename'], './attachments/')

def GetMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        print ('Message snippet: %s' % message['snippet'])

        return message
    except urllib2.HTTPError as e:
        print ('An error occurred: %s' % e)



def GetAttachments(service, user_id, attachments_id, message_id, filename, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
    attach_result = service.users().messages().attachments().get(userId=user_id, 
        id=attachments_id, messageId=message_id).execute()
    path = ''.join([store_dir, filename])
    file_data = base64.urlsafe_b64decode(attach_result['data']
                                                .encode('UTF-8'))

    f = open(path, 'wb')
    f.write(file_data)
    f.close()                    

  except urllib2.HTTPError as e:
    print ('An error occurred: %s' % error)

if __name__ == '__main__':
    main()
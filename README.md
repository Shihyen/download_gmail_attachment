# download_gmail_attachment

### Init

1. 建立cert, attachments 目錄
2. 將cw-gmail-oauth-credential.json放到cert底下

### Reference 

    https://developers.google.com/gmail/api/quickstart/python

### Install the Google Client Library
```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Use Service Account

1. create a service account: https://console.developers.google.com/iam-admin/serviceaccounts/
2. in options, create a key: this key is your usual client_secret.json - use it the same way
3. add owner permission to this service account (Member name = service account ID = service account email ex: thomasapp@appname-201813.iam.gserviceaccount.com
4. copy the email address of your service account = service account ID
5. simply go in your browser to the Google sheet you want to interact with
6. go to SHARE on the top right of your screen
7. go to advanced settings and share it with email address of your service account ex: thomasapp@appname-201813.iam.gserviceaccount.com


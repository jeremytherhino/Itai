import firebase_admin
from firebase_admin import credentials, auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class FirebaseAuthManager:
    def __init__(self):
        # Initialize Firebase Admin with the provided credentials file
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)

    def google_sign_in(self):
        # This method handles Google sign-in using OAuth 2.0
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', scopes=['https://www.googleapis.com/auth/userinfo.email',
                                          'https://www.googleapis.com/auth/userinfo.profile', 'openid'])
        creds = flow.run_local_server(port=0)

        # Get the user info from the credentials
        user_info = auth.verify_id_token(creds.id_token)
        return user_info


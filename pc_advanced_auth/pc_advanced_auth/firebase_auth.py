import pyrebase

import google.oauth2.credentials
import google_auth_oauthlib.flow

config = {
    "apiKey": "AIzaSyDTABVuIxLZPdyjWvmjqtz5zEypsM6yFHE",
    "authDomain": "advanced-authentication-c7d00.firebaseapp.com",
    "projectId": "advanced-authentication-c7d00",
    "storageBucket": "advanced-authentication-c7d00.appspot.com",
    "messagingSenderId": "392186055418",
    "appId": "1:392186055418:web:2689581d4cc8c9ae605743",
    "databaseURL": "",
}


firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "./client_secret.json",
    scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"],
)

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = "https://www.example.com/oauth2callback"

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type="offline",
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes="true",
)

import msal
from flask import Flask, render_template, request
import os
import http.client, urllib.parse
import requests
import json

app = Flask(__name__)

app.config.update(
    Instance="https://login.microsoftonline.com/",
    TenantId="0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c",
    ClientId="2337305b-1ccf-424d-b7f0-62878d0f2e9e",
    AppSecret="v.Q7Q~Hz4~41DCXbCr6dNgVoq2fNO0SAwulNT",
    ApplicationIdURI="api://5e91-2804-14c-bf2f-a532-2c00-934a-577e-c8be.ngrok.io/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c",
    AuthUrl="/oauth2/v2.0/token",
    ValidIssuers="https://login.microsoftonline.com/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c/v2.0,https://sts.windows.net/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c/"
)

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/GetUserAccessToken")
def GetUserAccessToken():
    idToken = get_token_auth_header()
    body = f'assertion={idToken}&requested_token_use=on_behalf_of&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_id={app.config["ClientId"]}@{app.config["TenantId"]}&client_secret={app.config["AppSecret"]}&scope=https://graph.microsoft.com/User.Read';
    try:
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        encoded_data = body.encode('utf-8')
        url = app.config["Instance"] + app.config["TenantId"] + app.config["AuthUrl"]
        r = requests.post(url, data=encoded_data,
                        headers=headers,
                        auth=requests.auth.HTTPBasicAuth("user", "password"))

        if (r.status_code == 200):
            responseBody = r.content
        else:
            responseBody = r.content
            raise Exception(responseBody)

        return json.loads(responseBody)["access_token"]
    except Exception as ex:
        return ex.Message;

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token

@app.route("/Auth/Start")
def auth_start():
    return render_template('AuthStart.html', AzureClientId = app.config["ClientId"])

@app.route("/Auth/End")
def auth_end():
    return render_template('AuthEnd.html')


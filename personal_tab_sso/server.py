import msal
from flask import Flask, render_template, request
import os
import http.client, urllib.parse
import requests
import json

app = Flask(__name__)

with open('config.json') as f:
    config = json.load(f)

app.config.update(config)

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
    return render_template('auth_start.html', AzureClientId = app.config["ClientId"])

@app.route("/Auth/End")
def auth_end():
    return render_template('auth_end.html')


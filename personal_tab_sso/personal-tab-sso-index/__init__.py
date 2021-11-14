import logging

import azure.functions as func 
from flask import Flask, render_template, render_template_string, request
import requests
import mimetypes
# from functionserver import app
import json
import sys
import html

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

# with open('config.json') as f:
#     config = json.load(f)

# app.config.update(config)

app_config = {
  'Instance': 'https://login.microsoftonline.com/',
  'TenantId': '0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c',
  'ClientId': '2337305b-1ccf-424d-b7f0-62878d0f2e9e',
  'AppSecret': 'v.Q7Q~Hz4~41DCXbCr6dNgVoq2fNO0SAwulNT',
  'ApplicationIdURI': 'api://0bd3-2804-14c-bf2f-a532-55b5-3ec6-ab00-9476.ngrok.io/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c',
  'AuthUrl': '/oauth2/v2.0/token',
  'ValidIssuers': 'https://login.microsoftonline.com/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c/v2.0,https://sts.windows.net/0ec7eb2f-a6b5-4cd1-9695-3f3ec151ed0c/'
}


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-index")
def index():
    index_template_file = f"{this.function_directory}/templates/index.html"
    auth_js_file = f"{this.function_directory}/static/js/auth.js"
    index_template = ''
    auth_js = ''

    with open(index_template_file, 'rb') as f:
        index_template = f.read().decode("utf-8")
    
    with open(file=auth_js_file, mode='r', encoding='utf-8') as f:
        auth_js = f.read()

    return render_template_string(index_template, auth_js=auth_js)

@app.route("/GetUserAccessToken")
def GetUserAccessToken():
    idToken = get_token_auth_header()
    body = f'assertion={idToken}&requested_token_use=on_behalf_of&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_id={app_config["ClientId"]}@{app_config["TenantId"]}&client_secret={app_config["AppSecret"]}&scope=https://graph.microsoft.com/User.Read';
    try:
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        encoded_data = body.encode('utf-8')
        url = app_config["Instance"] + app_config["TenantId"] + app_config["AuthUrl"]
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
    return render_template('auth_start.html', AzureClientId = app_config["ClientId"])

@app.route("/Auth/End")
def auth_end():
    return render_template('auth_end.html')


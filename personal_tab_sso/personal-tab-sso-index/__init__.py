import azure.functions as func 
from flask import Flask, render_template, render_template_string, request
import requests
import json
import sys
import os

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-index")
def index():
    index_template_file = f"{this.function_directory}/templates/index.html"
    auth_js_file = f"{this.function_directory}/static/js/auth.js"
    index_template = ''
    auth_js = ''

    with open(index_template_file, 'r') as f:
        index_template = f.read()
    
    with open(file=auth_js_file, mode='r') as f:
        auth_js = f.read()

    return render_template_string(index_template, auth_js=auth_js)

@app.route("/GetUserAccessToken")
def GetUserAccessToken():
    idToken = get_token_auth_header()
    body = f'assertion={idToken}&requested_token_use=on_behalf_of&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_id={os.environ.get("ClientId")}@{os.environ.get("TenantId")}&client_secret={os.environ.get("AppSecret")}&scope=https://graph.microsoft.com/User.Read';
    try:
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        encoded_data = body.encode('utf-8')
        url = os.environ.get("Instance") + os.environ.get("TenantId") + os.environ.get("AuthUrl")
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
    return render_template('auth_start.html', AzureClientId = os.environ.get("ClientId"))

@app.route("/Auth/End")
def auth_end():
    return render_template('auth_end.html')


import azure.functions as func 
from flask import Flask, request
import requests
import json
import sys
import os

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/GetUserAccessToken")
def GetUserAccessToken():
    try:
        idToken = get_token_auth_header()
        body = f'assertion={idToken}&requested_token_use=on_behalf_of&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_id={os.environ.get("ClientId")}@{os.environ.get("TenantId")}&client_secret={os.environ.get("AppSecret")}&scope=https://graph.microsoft.com/User.Read';
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
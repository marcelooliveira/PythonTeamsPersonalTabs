from flask import Flask
import azure.functions as func 
from flask import Flask
import sys

from ssoAuthHelper import GetAccessTokenOnBehalfUser

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/GetUserAccessToken")
def GetUserAccessToken():
    return GetAccessTokenOnBehalfUser()
    
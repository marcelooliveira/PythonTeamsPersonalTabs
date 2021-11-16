import azure.functions as func 
from flask import Flask, render_template_string
import sys
import os
from cacheHelper import CacheHelper

app = Flask(__name__)

this = sys.modules[__name__]
this.cacheHelper = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if this.cacheHelper is None:
        this.cacheHelper = CacheHelper(context.function_directory)
    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-auth-end")
def index():
    auth_end_template = this.cacheHelper.get_file("/templates/auth_end.html")
    auth_js = this.cacheHelper.get_file("/static/js/auth.js")

    return render_template_string(auth_end_template, AzureClientId=os.environ.get("ClientId"), context = { "AzureClientId": os.environ.get("ClientId"), "auth_js": auth_js })

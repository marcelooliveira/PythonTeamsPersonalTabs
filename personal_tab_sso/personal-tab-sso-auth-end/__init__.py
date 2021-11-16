import azure.functions as func 
from flask import Flask, render_template_string
import sys
import os

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-auth-end")
def index():
    auth_end_template_file = f"{this.function_directory}/templates/auth_end.html"
    auth_js_file = f"{this.function_directory}/static/js/auth.js"
    auth_end_template = ''
    auth_js = ''

    with open(auth_end_template_file, 'r') as f:
        auth_end_template = f.read()
    
    with open(file=auth_js_file, mode='r') as f:
        auth_js = f.read()

    return render_template_string(auth_end_template, AzureClientId=os.environ.get("ClientId"), context = { "AzureClientId": os.environ.get("ClientId"), "auth_js": auth_js })


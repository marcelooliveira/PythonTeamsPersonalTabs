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

@app.route("/api/personal-tab-sso-auth-start")
def auth_start():
    auth_start_template_file = f"{this.function_directory}/templates/auth_start.html"
    auth_js_file = f"{this.function_directory}/static/js/auth.js"
    auth_start_template = ''
    auth_js = ''

    with open(auth_start_template_file, 'r') as f:
        auth_start_template = f.read()
    
    with open(file=auth_js_file, mode='r') as f:
        auth_js = f.read()

    return render_template_string(auth_start_template, context = { "AzureClientId": os.environ.get("ClientId"), "auth_js": auth_js })

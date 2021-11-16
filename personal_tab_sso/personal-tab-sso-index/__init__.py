import azure.functions as func 
from flask import Flask, render_template_string
import sys
import os

cacheDisabled = (os.environ.get("CacheEnabled") == "false")
cache = dict()

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-index")
def index():
    index_template = get_file("/templates/index.html")
    auth_js = get_file("/static/js/auth.js")

    return render_template_string(index_template, auth_js=auth_js)

def get_file(file):
    path = f"{this.function_directory}{file}"
    if cacheDisabled or path not in cache:
        with open(path, 'r') as f:
            cache[path] = f.read()
    return cache[path]

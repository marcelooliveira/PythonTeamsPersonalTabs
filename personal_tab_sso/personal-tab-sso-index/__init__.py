import azure.functions as func 
from flask import Flask, render_template_string
import sys

cache = dict()

app = Flask(__name__)

this = sys.modules[__name__]
this.function_directory = None

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    this.function_directory = context.function_directory

    return func.WsgiMiddleware(app).handle(req, context)

@app.route("/api/personal-tab-sso-index")
def index():
    index_template = get_index_template()
    auth_js = get_auth_js()

    return render_template_string(index_template, auth_js=auth_js)

def get_index_template():
    file = f"{this.function_directory}/templates/index.html"
    if file not in cache:
        with open(file, 'r') as f:
            cache[file] = f.read()
    return cache[file]

def get_auth_js():
    file = f"{this.function_directory}/static/js/auth.js"
    # if file not in cache:
    with open(file, 'r') as f:
        cache[file] = f.read()
    return cache[file]


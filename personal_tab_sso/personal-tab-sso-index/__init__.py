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

@app.route("/api/personal-tab-sso-index")
def index():
    index_template = this.cacheHelper.get_file("/templates/index.html")
    auth_js = this.cacheHelper.get_file("/static/js/auth.js")

    return render_template_string(index_template, auth_js=auth_js)

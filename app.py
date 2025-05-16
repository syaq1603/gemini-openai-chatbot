#gemini

from flask import Flask, request, render_template
import google.generativeai as genai
from openai import OpenAI
import os
from markdown2 import Markdown

# Configure Gemini
gemini_api_key = os.environ["makersuite"]
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Configure OpenAI
openai_api_key = os.environ["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Gemini routes
@app.route("/gemini", methods=["GET", "POST"])
def gemini():
    return render_template("gemini.html")



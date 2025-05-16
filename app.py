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

@app.route("/gemini_reply", methods=["POST"])
def gemini_reply():
    q = request.form.get("q")
    r = model.generate_content(q)
    return render_template("gemini_reply.html", r=r.text)

# OpenAI routes
@app.route("/openai", methods=["GET", "POST"])
def openai():
    return render_template("openai.html")

@app.route("/openai_reply", methods=["POST"])
def openai_reply():
    q = request.form.get("q")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": q}]
    )
    r = response.choices[0].message.content

    markdowner = Markdown()
    formatted_response = markdowner.convert(r)
    return render_template("openai_reply.html", r=formatted_response)

if __name__ == "__main__":
    app.run(debug=True)

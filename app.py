#gemini

from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import os
import sqlite3
import datetime

gemini_api_key = 'AIzaSyCLuc4AhCtjvJBs9cOlB8r1v7p82CEh-pA'

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
app.secret_key = "mySecretKey123!"

first_time = 1

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global first_time
    if first_time==1:
        q = request.form.get("q")
        print(q)
        t = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into users(name,timestamp) values(?,?)",(q,t))
        conn.commit()
        c.close()
        conn.close()
        first_time=0
    return(render_template("main.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply", methods=["GET", "POST"])
def gemini_reply():
    q = request.form.get("q")
    print("Question received:", q)
    try:
        r = model.generate_content(q)
        response_text = r.text
    except Exception as e:
        print("Error:", e)
        response_text = "Sorry, an error occurred while generating the response."
    return render_template("gemini_reply.html", r=response_text)

@app.route("/user_log",methods=["GET","POST"])
def user_log():
    #read
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from users")
    r=""
    for row in c:
        print(row)
        r= r+str(row)
    c.close()
    conn.close()
    return(render_template("user_log.html",r=r))

@app.route("/delete_log",methods=["GET","POST"])
def delete_log():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from users")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete_log.html"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=False)
from flask import Flask, render_template, request, url_for, redirect



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# Test upload
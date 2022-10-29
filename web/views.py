from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import cgi

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/result", methods = [ "POST", "GET" ])
def result():
    # need to fix this one!!!
    if request.method == "POST":
        from actions import word_l
        form = cgi.FieldStorage()
        word_input = form.getvalue("word")
        if word_input in word_l:
            return f"We have {word_input} in our dictionary!"
        from actions import word_summary, word_matrixs
        return render_template("result.html", result = [word_summary, word_matrixs])
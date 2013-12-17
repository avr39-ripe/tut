#!/usr/bin/env python

from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/change", methods=['POST'])
def change():
    if request.method == 'POST':
        # Get the value from the submitted form
        lcdText = request.form['lcd']
        print "---Message is", lcdText

    else:
        lcdText = None
    return render_template('index.html', value=lcdText)


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')

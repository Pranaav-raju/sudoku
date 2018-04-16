from flask import Flask, url_for, request
from flask import render_template
import board

app = Flask(__name__)

@app.route('/')
def index():
    row1 = request.args.get('row1', '')
    row1 += "0" * 72
    try:
        print board.Board.string_to_array(row1)
    except ValueError:
        print "Board {} is not 81 characters.".format(row1)
    return render_template('index.html')
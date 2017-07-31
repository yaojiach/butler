import sqlite3
from db import LiteDB
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    ldb = LiteDB()
    d = ldb.get_one()
    return render_template('index.html', title='Butler', 
                           timestamp=d['ts'], state=d['st'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


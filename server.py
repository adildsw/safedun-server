import os
import shutil

from backend import safedun
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    os.mkdir('temp/')

    file = request.files['file']
    file.save('temp/input.png')

    mode = request.form['mode']
    key = request.form['key']
    cycle = int(request.form['cycle'])
    path = 'temp/input.png'

    obj = safedun(mode, key, cycle, path)
    obj.run()

    return send_file('temp\\output.png', attachment_filename='output.png')

if __name__ == "__main__":
    app.run(host="192.168.0.101", port="5000", debug=True)

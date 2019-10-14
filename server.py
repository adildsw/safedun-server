import argparse
import socket

from backend import safedun
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    mode = request.form['mode']
    key = request.form['key']
    cycle = int(request.form['cycle'])
    file = request.files['file']

    obj = safedun(mode, key, cycle, file)
    output_file = obj.run()

    return send_file(output_file, as_attachment=True, attachment_filename="output.png")

if __name__ == "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())

    parser  = argparse.ArgumentParser(description="safedun Server Option Description")
    parser.add_argument("-H", "--host", help="specify IP address to host server", required=False, default=host_ip)
    parser.add_argument("-p", "--port", help="specify Port number to host server", required=False, default="5000")
    parser.add_argument("-d", "--debug", help="specify whether the server will run on debug mode", required=False, default=False)
    parser.add_argument("-l", "--local", help="host server in localhost", required=False, default=False)

    argument = parser.parse_args()

    if not argument.local == False:
        argument.host = '127.0.0.1'

    app.run(host=argument.host, port=argument.port, debug=argument.debug)

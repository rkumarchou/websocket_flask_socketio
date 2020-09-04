# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

# [START gae_flex_websockets_app]
from flask import Flask, render_template
from flask_sockets import Sockets
from flask_socketio import SocketIO, emit, leave_room, join_room




app = Flask(__name__)
socketio = SocketIO(app)
sockets = Sockets(app)


@sockets.route('/chat')
def chat_socket(ws):
    print(dir(ws))
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        # Send the message to all clients connected to this webserver
        # process. (To support multiple processes or instances, an
        # extra-instance storage or messaging system would be required.)
        clients = ws.handler.server.clients.values()
        for client in clients:
            client.ws.send(message)
# [END gae_flex_websockets_app]


@socketio.on('client_message')
def receive_message (request_data):
    # request_data = json.loads(request.data)

    data = request_data['msg']
    socketio.emit('server_message', data)


@socketio.on('join')
def join(request_data):
    room = request_data.get('room', '')
    if room:
        leave_room(room)
    join_room(request_data.get('room'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app ,host="0.0.0.0", port="5000", debug=True)
    xxxxxx
    print("""
This can not be run directly because the Flask development server does not
support web sockets. Instead, use gunicorn:

gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app

""")

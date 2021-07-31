from turbo_flask import Turbo
from flask_sock import Sock, ConnectionClosed
from flask_login import current_user


class MyTurbo(Turbo):
    def init_app(self, app):
        ws_route = app.config.setdefault('TURBO_WEBSOCKET_ROUTE',
                                         '/turbo-stream')
        if ws_route:
            self.sock = Sock()

            @self.sock.route(ws_route)
            def turbo_stream(ws):
                user_id = self.user_id_callback()
                if user_id not in self.clients:
                    self.clients[user_id] = []
                self.clients[user_id].append(ws)
                try:
                    while True:
                        ws.receive(timeout=10)
                except ConnectionClosed:
                    self.clients[user_id].remove(ws)
                    if not self.clients[user_id]:
                        print(f'Client {user_id} will delete.{current_user =}')
                        del self.clients[user_id]

            self.sock.init_app(app)
        app.context_processor(self.context_processor)
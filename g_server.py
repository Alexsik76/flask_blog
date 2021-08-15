from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import create_app

app = create_app()
WSGIServer(('127.0.0.1', 5000), app).serve_forever()

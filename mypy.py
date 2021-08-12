from app.models import User, Post
from app import db, create_app


app = create_app(config='base_config')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

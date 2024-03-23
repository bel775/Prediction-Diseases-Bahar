from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2<?,}p46#6A7SS7z5A1k%VE*&m)O|?'

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    return app
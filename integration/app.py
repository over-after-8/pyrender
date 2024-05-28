from flask import Flask
from render.www.app import create_app

if __name__ == '__main__':
    app = Flask(__name__)
    app = create_app(app)


    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'


    app.run()

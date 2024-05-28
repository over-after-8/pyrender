from flask import Flask
from flask_login import login_required
from flask_wtf import CSRFProtect

from render.www.app import create_app

main_app = Flask(__name__)


@main_app.route('/')
@login_required
def index():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    WTF_CSRF_SECRET_KEY = 'secret_key'

    main_app = create_app(main_app)

    main_app.secret_key = WTF_CSRF_SECRET_KEY

    csrf = CSRFProtect()
    csrf.init_app(main_app)

    main_app.run(debug=True)

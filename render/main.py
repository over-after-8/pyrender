from flask import Flask, render_template
from flask_login import login_required
from flask_wtf import CSRFProtect

from render.www.app import create_app

main_app = Flask(__name__)


@main_app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("render/index.html")


def start(main_app):
    WTF_CSRF_SECRET_KEY = 'secret_key'

    main_app = create_app(main_app, [])

    main_app.secret_key = WTF_CSRF_SECRET_KEY

    csrf = CSRFProtect()
    csrf.init_app(main_app)

    main_app.run(port=5000, debug=True, host='0.0.0.0')


if __name__ == '__main__':
    start(main_app)

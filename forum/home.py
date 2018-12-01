from flask.blueprints import Blueprint
from flask import render_template


bp_home = Blueprint('home', __name__, url_prefix='/')


@bp_home.route('/')
def home():
    return render_template('index.html')

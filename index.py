from flask import Blueprint, render_template
bp = Blueprint('main', __name__)

# Define a route and the corresponding function to handle it
@bp.route('/')
def index():
    return render_template('index.html',title = 'index')

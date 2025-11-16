from flask import *
from datetime import datetime

bp = Blueprint('views', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
@bp.route('/casa')
def index():
    """Renders the landing page."""
    return render_template('landpage/index.html',
        current_yerar=datetime.now().year
    )

@bp.route('/about')
def about():
    """Renders the about page."""
    return render_template('landpage/about.html')

@bp.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('landpage/contact.html')

@bp.route('/help')
def help_page():
    """Renders the help page."""
    return render_template('landpage/help.html')

@bp.route('/services')
def services():
    """Renders the services page."""
    return render_template('landpage/services.html')
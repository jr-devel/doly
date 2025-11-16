from flask import *
from datetime import datetime
from app.auth import login_required

bp = Blueprint('views_client', __name__, url_prefix='/client')

@bp.route('/dashboard')
@login_required
def dashboard() -> Response:
    """Renders the client dashboard page."""
    # Here you would typically fetch client-specific data from the database
    return render_template('client/dashboard.html',
        current_year=datetime.now().year,
        id_client=id_client
    )
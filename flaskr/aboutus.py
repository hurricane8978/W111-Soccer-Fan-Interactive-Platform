from flask import render_template,request,Blueprint

bp = Blueprint('aboutus',__name__)

@bp.route('/aboutus')
def aboutus():
    # More to come!
    return render_template('aboutus.html')

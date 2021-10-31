from flask import Blueprint, render_template
from calculated_distance.forms import CalculateDistanceForm

calculated_distance = Blueprint('calculated_distance', __name__, template_folder='templates')


@calculated_distance.route('/', methods = ['POST'])
def index():
    form = CalculateDistanceForm()
    return render_template('calculated_distance/index.html', form=form)

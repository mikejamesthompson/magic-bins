from flask.ext.wtf import Form
from wtforms import TextField, validators

class SearchForm(Form):
    road = TextField('road', validators = [validators.Required()])
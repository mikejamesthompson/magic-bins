from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class SearchForm(Form):
    road = TextField('road', validators = [Required()])
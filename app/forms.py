from flask.ext.wtf import Form
from wtforms import fields, validators

class SearchForm(Form):
    road = fields.StringField(u'road', validators = [validators.InputRequired(), validators.Length(min=1,message="Please enter a road name")])
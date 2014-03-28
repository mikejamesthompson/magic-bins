from flask import render_template, flash, request, redirect, url_for
from app import app, helpers, forms, models

from webhelpers.text import urlify
from datetime import datetime


# Homepage with search form
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = forms.SearchForm()
	return render_template("index.html", form = form)


# Search page for people devices/browsers without javascript
@app.route('/search', methods = ['GET', 'POST'])
def search():
	form = forms.SearchForm()
	if form.validate_on_submit():
		roads = models.Location.query.filter(Location.name.ilike('%'+form.road.data+'%')).all()
		return render_template('search.html', form = form, roads = roads)
	else:
		flash("Please enter a road name")
		return render_template('search.html', form = form)


# Nothing to see here
@app.route('/collection-times')
def collections_index():
	return redirect(url_for('index'))


# Page for an individual road
@app.route('/collection-times/<road>')
def collections(road):
	
	location = models.Location.query.filter_by(url_name = urlify(road)).first()
	collections = location.collections

	cs = []
	frequencies = { 7 : 'Weekly', 14 : 'Fortnightly' }

	for collection in collections:

		next, shift = collection.next_collection(datetime.today(), collection.reference_date, collection.frequency)

		cs.append({
			'name' : collection.type,
			'frequency' : frequencies[collection.frequency],
			'next' : next,
			'shift' : shift
			})


	return render_template('collections.html', road=location, collections=cs)

# Static pages
@app.route('/about')
@app.route('/contact')
def static_page():
	return render_template("static.html")
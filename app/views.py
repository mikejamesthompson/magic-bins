from flask import render_template, flash, request, redirect, url_for
from app import app, helpers, forms
from app.models import Location

from webhelpers.text import urlify
from datetime import datetime, date

@app.errorhandler(500)
def internal_error(exception):
	app.logger.exception(exception)
	return render_template('static.html'), 500

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
		roads = Location.query.filter(Location.name.ilike('%'+form.road.data+'%')).all()
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
	
	location = Location.query.filter_by(url_name = urlify(road)).first()
	collections = location.collections

	if (request.args.get("date")):
		check_date = datetime.strptime(request.args.get("date"), "%Y-%m-%d").date()
	else:
		check_date = date.today()

	cs = []
	frequencies = { 7 : 'Weekly', 14 : 'Fortnightly' }

	schedule_changed = False

	for collection in collections:

		next, next_changed = collection.next_collection(check_date, collection.reference_date, collection.frequency)

		if (next_changed):
			schedule_changed = True

		cs.append({
			'name' : collection.type,
			'frequency' : frequencies[collection.frequency],
			'next' : next,
			'next_changed' : next_changed
			})


	return render_template('collections.html', road=location, collections=cs, schedule_changed=schedule_changed)

# Static pages
@app.route('/about')
@app.route('/contact')
def static_page():
	return render_template("static.html")

from flask import render_template, flash, request, redirect, url_for
from app import app, helpers, forms
from app.models import Location

from webhelpers.text import urlify
from datetime import datetime, date

@app.errorhandler(500)
def internal_error(exception):
	app.logger.exception(exception)
	return render_template('500.html'), 500

@app.errorhandler(404)
def not_found_error(exception):
	app.logger.exception(exception)
	return render_template('404.html'), 404


# Homepage with search form
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = forms.SearchForm(csrf_enabled=False)
	return render_template("index.html", form = form)


# Search page for people devices/browsers without javascript
@app.route('/search')
def search():
	form = forms.SearchForm(request.args,csrf_enabled=False)
	if form.validate():
		search_string = form.data.get("road")
		roads = Location.query.filter(Location.name.ilike('%'+search_string+'%')).all()
		return render_template('search.html', 
			form = form,
			roads = roads,
			title = "Finding bin collections for roads matching " + search_string,
			body="search")
	else:
		flash(u'Please enter a road name', 'error')
		return redirect(url_for('index'))


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


	return render_template('collections.html', 
		road=location,
		collections=cs,
		schedule_changed=schedule_changed,
		title="Bin collections for " + location.name + ", " + location.area,
		body="collections")

# Static pages
@app.route('/about')
@app.route('/contact')
def static_page():
	
	return render_template("static.html", body="static")

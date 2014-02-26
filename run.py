from app import app

app.debug = True

if app.debug:
	import logging
	from logging import FileHandler
	file_handler = FileHandler('app.log')
	file_handler.setLevel(logging.WARNING)
	app.logger.addHandler(file_handler)

app.run(debug = app.debug)

# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

application = Flask(__name__) #create the application instance
application.config.from_object(__name__) #Load config from this file , blog.py

# Load default config and override config from an environment variable
application.config.update(dict(
	DATABASE=os.path.join(application.root_path, 'blog.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
application.config.from_envvar('BLOG_SETTINGS', silent=True)

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(application.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with application.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@application.cli.command('initdb')
def initdb_command():
	"""Initializes the database."""
	init_db()
	print('Initialized the database.')

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context."""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@application.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()












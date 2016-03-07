# ----- Imports ----- #

import markdown


# ----- Setup ----- #

Markdown = markdown.Markdown(extensions=['meta'])


# ----- Engine Class ----- #

class Engine():

	"""The main Engine object, used to generate the static site from source."""

	_articles_dir = 'articles'

	def __init__(self, src='content', build='build'):

		self._src = src
		self._build = build

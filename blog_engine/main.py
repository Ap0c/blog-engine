# ----- Imports ----- #

import markdown


# ----- Setup ----- #

Markdown = markdown.Markdown(extensions=['meta'])


# ----- Engine Class ----- #

class Engine():

	"""The main Engine object, used to generate the static site from source."""

	_articles_dir = 'articles'
	_articles_url = '/' + _articles_dir + '/'

	def __init__(self, src='content', build='build'):

		"""Sets up source and build directories."""

		self._src = src
		self._build = build

	@property
	def articles_dir(self):

		"""Getter for the articles build directory."""

		return self._articles_dir

	@articles_dir.setter
	def articles_dir(self, value):

		"""Sets the name in the build directory for articles."""

		self._articles_dir = value
		self._articles_url = '/' + value + '/'

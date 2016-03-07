# ----- Imports ----- #

import os
import shutil
import markdown


# ----- Setup ----- #

md = markdown.Markdown(extensions=['meta'])


# ----- Engine Class ----- #

class Engine():

	"""The main Engine object, used to generate the static site from source."""

	_articles_build_dir = 'articles'
	_articles_url = '/' + _articles_build_dir + '/'
	_articles_src_dir = 'articles'

	def __init__(self, src='content', build='build'):

		"""Sets up source and build directories."""

		self._src = src
		self._build = build

	@property
	def articles_build_dir(self):

		"""Getter for the articles build directory."""

		return self._articles_build_dir

	@articles_build_dir.setter
	def articles_build_dir(self, value):

		"""Sets the name in the build directory for articles."""

		self._articles_build_dir = value
		self._articles_url = '/' + value + '/'

	def build(self):

		"""Builds the static site, saves to build directory."""

		articles_src_dir = os.path.join(self._src, self._articles_src_dir)

		for article in os.listdir(articles_src_dir):

			filename = article + '.md'
			filepath = os.path.join(articles_src_dir, article, filename)

			input_dir = os.path.join(self._src, self._articles_src_dir, article)
			output_dir = os.path.join(self._build, self._articles_build_dir, article)
			output_file = os.path.join(output_dir, article + '.html')

			shutil.copytree(input_dir, output_dir, ignore=lambda p, f: [filename])

			with open(filepath, 'r') as f:

				page = md.convert(f.read())

				with open(output_file, 'w') as outf:
					outf.write(page)

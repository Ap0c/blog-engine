# ----- Imports ----- #

import os
import shutil
import markdown


# ----- Setup ----- #

SCRIPT_TAG = '\n<script type="text/javascript" src="./{}"></script>'


# ----- Functions ----- #

def render_article(input_file, output_file):

	"""Renders a markdown file to a given output file."""

	md = markdown.Markdown(extensions=['meta'])

	with open(input_file, 'r') as f:
		page = md.convert(f.read())

	if 'scripts' in md.Meta:

		for script in md.Meta['scripts']:
			page += SCRIPT_TAG.format(script)

	with open(output_file, 'w') as outf:
		outf.write(page)


def remove_build(build_dir):

	"""Wipes the previous build directory."""

	try:
		shutil.rmtree(build_dir)
	except FileNotFoundError:
		pass


# ----- Article Class ----- #

class Article():

	"""An article object, for rendering a specific article."""

	def __init__(self, name, parent_dir, build_dir):

		self._name = name
		self._filename = name + '.md'
		self._src_dir = os.path.join(parent_dir, name)
		self._filepath = os.path.join(parent_dir, name, self._filename)
		self._build_dir = os.path.join(build_dir, name)
		self._build_file = os.path.join(self._build_dir, name + '.html')

	def build(self):

		"""Builds an article from source, and copies static files across."""

		shutil.copytree(self._src_dir, self._build_dir,
				ignore=lambda p, f: [self._filename])

		render_article(self._filepath, self._build_file)


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

		remove_build(self._build)

		articles_src_dir = os.path.join(self._src, self._articles_src_dir)
		articles_build_dir = os.path.join(self._build, self._articles_build_dir)

		for article in os.listdir(articles_src_dir):

			article = Article(article, articles_src_dir, articles_build_dir)
			article.build()

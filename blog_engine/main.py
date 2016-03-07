# ----- Imports ----- #

import os
import pkg_resources as pkg
import shutil
import markdown
from jinja2 import Template


# ----- Setup ----- #

SCRIPT_TAG = '\n<script type="text/javascript" src="./{}"></script>'
LINK_TAG = '<link rel="stylesheet" href="./{}">'

TEMPLATE_FILENAME = 'base.html'
DEFAULT_TEMPLATE = pkg.resource_filename(__name__, TEMPLATE_FILENAME)
DEFAULT_TITLE = 'My Blog'


# ----- Functions ----- #

def read_template(filename):

	"""Reads a Jinja2 template from file."""

	with open(filename, 'r') as base_templ:
		template = Template(base_templ.read())

	return template


def render_article(input_file, output_file, template):

	"""Renders a markdown file to a given output file."""

	md = markdown.Markdown(extensions=['meta'])

	with open(input_file, 'r') as f:
		page = md.convert(f.read())

	if 'scripts' in md.Meta:

		for script in md.Meta['scripts']:
			page += SCRIPT_TAG.format(script)

	if 'stylesheets' in md.Meta:

		head = ''

		for stylesheet in md.Meta['stylesheets']:
			head += LINK_TAG.format(stylesheet)

	title = md.Meta['title'][0] if 'title' in md.Meta else DEFAULT_TITLE
	rendered = template.render(content=page, title=title, head=head)

	with open(output_file, 'w') as outf:
		outf.write(rendered)


def remove_build(build_dir):

	"""Wipes the previous build directory."""

	try:
		shutil.rmtree(build_dir)
	except FileNotFoundError:
		pass


# ----- Article Class ----- #

class Article():

	"""An article object, for rendering a specific article."""

	def __init__(self, name, parent_dir, build_dir, template):

		self._name = name
		self._filename = name + '.md'
		self._src_dir = os.path.join(parent_dir, name)
		self._filepath = os.path.join(parent_dir, name, self._filename)
		self._build_dir = os.path.join(build_dir, name)
		self._build_file = os.path.join(self._build_dir, name + '.html')
		self._template = template

	def build(self):

		"""Builds an article from source, and copies static files across."""

		shutil.copytree(self._src_dir, self._build_dir,
				ignore=lambda p, f: [self._filename])

		render_article(self._filepath, self._build_file, self._template)


# ----- Engine Class ----- #

class Engine():

	"""The main Engine object, used to generate the static site from source."""

	_articles_build_dir = 'articles'
	_articles_url = '/' + _articles_build_dir + '/'
	_articles_src_dir = 'articles'

	def __init__(self, src='content', build='build', template=None):

		"""Sets up source and build directories."""

		self._src = src
		self._build = build

		if template:
			self._template = read_template(template)
		else:
			self._template = read_template(DEFAULT_TEMPLATE)

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

			article = Article(article, articles_src_dir, articles_build_dir,
				self._template)
			article.build()

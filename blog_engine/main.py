# ----- Imports ----- #

import os
import pkg_resources as pkg
import shutil
import markdown
from jinja2 import Template


# ----- Setup ----- #

_SCRIPT_TAG = '\n<script type="text/javascript" src="./{}"></script>'
_LINK_TAG = '<link rel="stylesheet" href="./{}">'

_TEMPLATE_DIR = 'templates'
_TEMPLATES_PATH = pkg.resource_filename(__name__, _TEMPLATE_DIR)
_BASE_TEMPLATE = os.path.join(_TEMPLATES_PATH, 'base.html')
_LIST_TEMPLATE = os.path.join(_TEMPLATES_PATH, 'list.html')

_DEFAULT_TITLE = 'My Blog'


# ----- Functions ----- #

def _read_template(filename):

	"""Reads a Jinja2 template from file."""

	with open(filename, 'r') as base_templ:
		template = Template(base_templ.read())

	return template


def _static_files(page, metadata):

	"""Adds links to static files (js, css) to the page."""

	head = ''

	if 'scripts' in metadata:

		for script in metadata['scripts']:
			page += _SCRIPT_TAG.format(script)

	if 'stylesheets' in metadata:

		for stylesheet in metadata['stylesheets']:
			head += _LINK_TAG.format(stylesheet)

	return head, page


def _render_article(input_file, output_file, template):

	"""Renders a markdown file to a given output file."""

	md = markdown.Markdown(extensions=['meta'])

	with open(input_file, 'r') as f:
		page = md.convert(f.read())

	head, page = _static_files(page, md.Meta)
	title = md.Meta['title'][0] if 'title' in md.Meta else _DEFAULT_TITLE

	rendered = template.render(content=page, title=title, head=head)

	with open(output_file, 'w') as outf:
		outf.write(rendered)


def _build_article(name, parent_dir, build_dir, template):

	"""Builds an individual article."""

	filename = name + '.md'
	src_dir = os.path.join(parent_dir, name)
	filepath = os.path.join(parent_dir, name, filename)
	build_dir = os.path.join(build_dir, name)
	build_file = os.path.join(build_dir, name + '.html')

	shutil.copytree(src_dir, build_dir, ignore=lambda p, f: [filename])

	_render_article(filepath, build_file, template)


def _remove_build(build_dir):

	"""Wipes the previous build directory."""

	try:
		shutil.rmtree(build_dir)
	except FileNotFoundError:
		pass


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
			self._template = _read_template(template)
		else:
			self._template = _read_template(_BASE_TEMPLATE)

	def _build_articles(self):

		"""Builds all the articles in the static site."""

		articles_src_dir = os.path.join(self._src, self._articles_src_dir)
		articles_build_dir = os.path.join(self._build, self._articles_build_dir)

		for article in os.listdir(articles_src_dir):

			_build_article(article, articles_src_dir, articles_build_dir,
				self._template)

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

		_remove_build(self._build)
		self._build_articles()

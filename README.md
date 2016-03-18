# Blog Engine

A simple tool for compiling a Markdown-based blog to a static site, written in Python 3.

## Install

Download a copy of the repository, navigate to the directory, optionally set up a virtual environment, and run:

```
python setup.py install
```

## Usage

```python
from blog_engine import Engine

ng = Engine()

ng.build()
```

## Layout

The source folder is expected to contain two directories, although the second is optional. The first of these contains the articles to be included in the site, and by default is expected to be named `articles`, although this can be change with the `articles_src_dir` method. Within this directory, each article is expected to be located in a subdirectory of the same name. For example, for an article named 'my-article', there will be a subdirectory named `my-article` containing a Markdown file called `my-article.md`. This subdirectory will also contain any additional assets that the article requires, such as scripts, stylesheets or images.

The second, optional directory, is called `site`, and contains any additional pages, scripts, stylesheets etc. that are to be available site-wide. So, for example, to create an 'about' page, you would create a file called `about.md` in the `site` directory, along with perhaps a stylesheet called `about.css`. This will then appear at the url `/about.html`.

The structure for an example source directory might look like this:

```
content/
    articles/
        article-one/
            article-one.md
            article-one.css
            article-one.js
    site/
        about.md
        about.css
```

### Markdown Metadata

The metadata feature of multi-markdown is used to provide information about the title and assets included within a page. This is best illustrated with an example Markdown document:

```
Title: Article One
Scripts: article-one.js
Stylesheets: article-one.css
    extra.css

# Article One

Lorem ipsum...
```

The `Title` key sets the page title. The `Scripts` and `Stylesheets` keys are for scripts and stylesheets to be included with the page (these must be in the same directory as the article). Multiple of each of these can be included by putting them on a newline with some whitespace.

## API

### class Engine(*src='content'*, *build='build'*)

All usage occurs via this `Engine` class.

- `src` (*optional*): The directory in which the site source files are to be found. For more information on the layout of this directory, please see Layout above.
- `build` (*optional*): The directory in which the site is to be built.

### Engine.build(*base_template=None*, *list_template=None*)

Builds the site from Markdown files. By default it will use the built-in base and list templates, but custom Jinja2 templates may also be specified.

- `base_template`: A Jinja2 template to use for the page boilerplate. If not specified the default will be used (`blog_engine/templates/base.html`). This template will be passed three variables:

    - `content`: The main page content, in HTML markup, which will appear within the `body` tag. For articles written in Markdown, this will be the article rendered to HTML.
    - `head`: Any scripts or stylesheets specified in the Markdown metadata section, converted to `script` and `link` tags.
    - `title`: Optional, the title of the page, will default to `My Blog` if not specified in the Markdown metadata.

- `list_template`: A Jinja2 template to use for the view displaying a list of articles. If not specified the default will be used (`blog_engine/templates/list.html`). It will be passed a single variable, `articles`, which is a list of dictionaries containing article information in the following format:

    - `name`: The name of the article.
    - `link`: The url of the article relative to the site domain (i.e. `/articles/article_name/article_name.html`).

### Engine.articles_build_dir
### Engine.articles_build_dir(*value*)

Getter and setter for the subdirectory in the build directory where articles are to be placed (Note: this will also be the URL of the articles in the final site). The default is `articles`.

### Engine.articles_src_dir
### Engine.articles_src_dir(*value*)

Getter and setter for the directory in the site source in which the articles are found. The default is `articles`.

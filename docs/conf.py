
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Wrap Dev Tools'
copyright = '2018, Charles Barto'
author = 'Charles Barto'
version = ''
release = ''
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.autoprogram',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints'
]
apidoc_output_dir = 'api'
apidoc_module_dir = '../wrapdevtools'
apidoc_seperate_modules = True
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_theme = 'alabaster'
htmlhelp_basename = 'WrapDevToolsdoc'
man_pages = [
    (master_doc, 'wrapdevtools', 'Wrap Dev Tools Documentation',
     [author], 1)
]

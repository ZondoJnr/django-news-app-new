# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django

sys.path.insert(0, r'C:\Users\zondo\OneDrive\Desktop\News App Docker\news_portal')
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_portal.settings'
django.setup()

project = 'NewsPortal'
copyright = '2025, Caleb Zondo'
author = 'Caleb Zondo'
release = '00.00.01'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
"sphinx.ext.autodoc",
"sphinx.ext.viewcode",
"sphinx.ext.napoleon"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

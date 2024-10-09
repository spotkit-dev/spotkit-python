# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('/Users/heath.ward/Dev/highspot_pro/spotkit'))

project = 'SpotKit'
copyright = '2024, SpotKit.dev'
author = 'SpotKit.dev'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# General configuration
extensions = [
    'sphinx.ext.autodoc',     # Automatically generates documentation from docstrings
    'sphinx.ext.napoleon',    # Supports Google-style docstrings
    'sphinx.ext.viewcode',    # Adds links to the source code in the documentation
]

# Napoleon settings to parse Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Output file base name for HTML help builder
htmlhelp_basename = 'spotkitdoc'

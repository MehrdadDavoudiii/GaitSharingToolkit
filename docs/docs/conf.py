import os
import sys

project = "Gait Sharing"
copyright = "2025, Mehrdad Davoudi"
author = "Mehrdad Davoudi"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_logo = "_static/images/logo.png"
html_favicon = "_static/images/logo.png"

html_theme_options = {
    "logo_only": False,

    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "navigation_depth": 3,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

html_context = {
    "display_github": True,
    "github_user": "MehrdadDavoudiii",
    "github_repo": "GaitSharingToolkit",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

html_show_sourcelink = False

### Python & Django related utilities

#### Overview

Just a few simple scripts to make my life easier.

#### Installation

	sudo easy_install jinja2 virtualenv pip
	git clone https://StefanKjartansson@github.com/StefanKjartansson/BinUtils.git
	symlink the utils you want to your bin folder

#### Utils

##### djappskeleton

Creates a auto-configured self-contained setuptools installable Django application:

1. Creates a directory for the application
2. Creates a virtual environment under application/env and installs Django (optionally installs nose, coverage & django nose).
3. Creates a Django test project, starts the application, moves it to the parent folder & patches the test settings.
4. Creates a patched setup.py:
	* Adds find_package_data, easier packaging of templates, fixtures & static content.
	* Adds setup.py Django test runner command, python setup.py test runs the application's unittests via the test project.
	* Auto-populates the install_requires with django (nose and coverage if specified).
5. If --git flag was present, initialises a git repo with a default .gitignore file 

###### TODO:

* Mercurial
* --tox option: Auto-configure tox
* --jenkins option: Auto-configure the xml plugins.
 

##### appskeleton

Does the same as djappskeleton, except no django, no testing. 

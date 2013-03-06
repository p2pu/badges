badges
======

This is our third take on badges! It boils down to this: Create a badge, submit a project for a badge, get feedback and revise your project, receive the badge, give feedback and build the value of the badge you have by being part of an awesome community around it!

## Installation

This project is written using django. To get up and running for development

1. Make a local copy of the code: ```git clone https://github.com/p2pu/badges```
1. Install python and virtualenv (changes are good you already have them)
1. Create a new virtual environment somewhere: ```virtualenv /path/to/somewhere```
1. Activate the virtual environment: ```source /path/to/somewhere/bin/activate```
1. Install dependancies: ```pip install -r /path/to/code/badges/requirements.txt```
1. Sync database: ```python /path/to/code/badges/badges/manage.py syncdb```
1. Load some test data: ```python /path/to/code/badges/badges/manage.py load_test_data /path/to/test/data```
1. Run development server: ```python /path/to/code/badges/badges/manage.py runserver```
1. Go to http://localhost:8000/ and play around
1. And lastly, fix all the bugs, and cool new features and take over the world :)

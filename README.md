Badges [![Build Status](https://travis-ci.org/ercchy/badges.png?branch=master)](https://travis-ci.org/ercchy/badges)
======

This is our third take on badges! It boils down to this: Create a badge, submit a project for a badge, get feedback and revise your project, receive the badge, give feedback and build the value of the badge you have by being part of an awesome community around it!

## Installation


This project is written using django. Most dependencies are handled by POP, but there are a few initial system requirements.
### System Requirements
The following packages need to be installed on your system:
* [Python](http://python.org) 2.7+
* [Virtualenv](http://virtualenv.org)
* [Git](http://git-scm.com)
* [PostgreSQL](http://postgresql.org) and PostgreSQL-dev
* [Ruby](http://ruby-lang.org)

### e.g. installation on Ubuntu Linux
Ruby and Python come pre-installed on Ubuntu Linux.

#### PostgreSQL
To install the additional dependencies on Ubuntu Linux, use a graphical package manager or the following commands in Terminal:
```sh
sudo apt-get install postgresql postgresql-server-dev-all
```

#### virtualenv
```sh
sudo pip install virtualenv
```

To complete the Virtualenv installation, follow the [virtualenv installation instructions](http://virtualenvwrapper.readthedocs.org/en/latest/install.html).

#### SASS
The SASS package can be installed through Ruby Gems.
```sh
sudo gem install sass
```


### Install Badges
To get up and running for development

#### Get the code
1. Make a local copy of the code: ```git clone https://github.com/p2pu/badges```
1. Init submodules: ```git submodule init```
1. Fetch submodules: ```git submodule update```

#### Create a virtual environment
1. Create a new virtual environment somewhere: ```virtualenv /path/to/somewhere```
1. Activate the virtual environment: ```source /path/to/somewhere/bin/activate```

#### Install additional dependencies
```sh
pip install -r /path/to/code/badges/requirements.txt
```

#### Create a local settings file
Copy settings_local.dist.py to settings_local.py
```sh
cp settings_local.dist.py settings_local.py
```
#### Set up the database
1. Sync database: ```python /path/to/code/badges/manage.py syncdb```
1. Load some test data: ```python /path/to/code/badges/manage.py load_test_data /path/to/code/testdata/test_data.json```

#### Start the server
1. Run development server: ```python /path/to/code/badges/manage.py runserver```
1. Go to http://localhost:8000/ and play around

#### Enjoy! 
And lastly, fix all the bugs, add cool new features and take over the world :)

### Mozilla Open Badge Integration and Development

Documentation:
* Badges/Technology https://wiki.mozilla.org/Badges/Technology
* Assertions https://github.com/mozilla/openbadges/wiki/Assertions

Setup Development Environment:
1. Prepare validator
  * user online http://validator.openbadges.org/
  * or install validator locally
    * $ install nodejs and npm
    * $ git clone https://github.com/mozilla/openbadges-validator-service.git
    * $ cd openbadges-validator-service
    * $ npm install
    * $ node app.js
    * point your browser to http://localhost:8888
1. Amend settings_local.py
   * set OPEN_BADGES_PUBLIC_URL to your development box (and later to production public url)
   * if using local validator, OPEN_BADGES_PUBLIC_URL='http://localhost:8000'
   * otherwise play with ssh remote tunneling and set OPEN_BADGES_PUBLIC_URL accordingly
1. Open Badges urls:
  * OPEN_BADGES_PUBLIC_URL/openbadges/assertions/<uid>
  * OPEN_BADGES_PUBLIC_URL/openbadges/badge/<badge_id>
  * OPEN_BADGES_PUBLIC_URL/openbadges/organisation



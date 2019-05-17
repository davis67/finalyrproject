# AUTOMATED CRIME REPORT VISUALISATION AND SECURE PATH PREDICTION

The partial code for my final project, *AUTOMATED CRIME REPORT VISUALISATION AND SECURE PATH PREDICTION*, which will be hosted with digital ocean soon.

## Installation and Set Up
Prerequisites:
* [Python 3](https://www.python.org/download/releases/3.6.7/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

Clone the repo from GitHub:
```
git clone https://github.com/davis67/finalyrproject.git
```

Create a virtual environment for the project and activate it:

```
linux/mac users ;- python3 -m venv venv
windows users ;- virtualenv venv
source venv/bin/activate
```

Install the required packages:
```
pip install -r requirements.txt
```

## Database configuration
You will need to create a MySQL user your terminal, as well as a MySQL database. Then, grant all privileges on your database to your user, like so:

```
$ mysql -u root

mysql> CREATE USER 'root'@'localhost' IDENTIFIED BY 'password_here';

mysql> CREATE DATABASE crimes_final_year_project;

mysql> GRANT ALL PRIVILEGES ON crimes_final_year_project . * TO 'root'@'localhost';
```

Note that you can use sqlite, postgres or any other.Dont be limited to mysql. After creating the database, run migrations as follows:

* `flask db init`
* `flask db migrate`
* `flask db upgrade`

## instance/config.py file
Create a directory, `instance`, and in it create a `config.py` file. This file should contain configuration variables that should not be publicly shared, such as passwords and secret keys. The app requires you to have the following configuration
variables:
* SECRET_KEY
* SQLALCHEMY_DATABASE_URI (`'mysql://user:password@localhost/database_name'`)

## Launching the Program
Set the FLASK_APP and FLASK_CONFIG variables as follows:

* `export FLASK_APP=run.py`
* `export FLASK_CONFIG=development`

## Registering the administrator
Open the application in your terminal and run the following commands:

* `flask shell`
* `from pathfinder.model import User`
* `from pathfinder import db`
* `admin = User(email="admin@admin.com", full_names="admin CrimeFinder", password="admin@123", is_admin=True)`
* `db.session.add(admin)`
* `db.session.commit()`

You can now run the app with the following command: `flask run` or `python -m flask run`
## Built With...
* [Flask](http://flask.pocoo.org/)

## Credits and License

Copyright (c) 2019 [davis67](https://github.com/davis67)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

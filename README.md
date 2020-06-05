# BGtrails
A collection of hikes in the Bulgarian mountains. All hikes include '.gpx' navigation files. 

## `You will need Python 3 and pip to run this project.`
## Creating virtual environment 
* Clone the repository from GitHub
```
git clone https://github.com/ivan4oto/BGtrails.git
```
* Enter the root file of the project
```
cd BGtrails/
```
* Create virtual environment with last argument name of the environment. For example `post` will be the name for our environment
```
python3 -m virtualenv post
```
* Activate virtual environment
```
source post/bin/activate
```

## Installation

* Install all project`s dependencies
```
 pip install -r requirements.txt
```
* Stage all models for migrations
```
 python3 manage.py makemigrations
```
* Apply all database migrations.Currently the default database is SQLite.
```
 python3 manage.py migrate
```
* If you need admin rights
```
python3 manage.py createsuperuser
```
* Start the local server. The default port is 8000 and the url is `http://127.0.0.1:8000/blog/`
```
python3 manage.py runserver
```

# Item Catalog

Udacity Full-stack Nanodegree 4th project


## Getting Started

We assume that you have `git` and `virtualenv` installed.
### Prerequisites

Item catalog depends on:
```
certifi==2017.4.17
chardet==3.0.4
click==6.7
Flask==0.12.2
Flask-SQLAlchemy==2.2
Flask-WTF==0.14.2
httplib2==0.10.3
idna==2.5
itsdangerous==0.24
Jinja2==2.9.6
MarkupSafe==1.0
oauth2client==4.1.1
pyasn1==0.2.3
pyasn1-modules==0.0.9
requests==2.17.3
rsa==3.4.2
six==1.10.0
SQLAlchemy==1.1.10
urllib3==1.21.1
Werkzeug==0.12.2
WTForms==2.1

```


### Installing

First clone the code

```
git clone https://github.com/ischizoid/item-catalog.git
```

Then CD into directory of item-catalog to create a virtual environment

```
cd item-catalog
virtualenv venv
```

then activate it

```
source venv/bin/activate
```
then install dependencies

```
pip install -r requirements.txt
```
finally run the following script to populate the database
```
python lotsofitems.py
```
End with an example of getting some data out of the system or using it for a little demo

### Run

Run the flask internal webserver at http://localhost:8000 by running
```
python run.py
```

Api endpoint is
```
http://localhost:8000/api/catalog.json
```

## Authors

* **Mostafa Azeem** - *Initial work* - [Ischizoid](https://github.com/ischizoid/)

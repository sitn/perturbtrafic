# PerturbTrafic

## Requirements

- Python 3.6 + pipenv
- PostgreSQL 10 + PostGIS 2.4.4
- Git


## Deploy

1. Clone this repository

```powershell
git clone https://github.com/sitn/perturbtrafic.git
cd perturbtrafic
```

2. In the folder `apache`, edit `app.wsgi` and `wsgi.conf` with the paths where your api is located.

3. Install the api

```powershell
cd back
$env:PIPENV_VENV_IN_PROJECT="true"
pipenv install
pipenv shell
pip install -e .
```

4.
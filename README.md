# PerturbTrafic

## Requirements

- Python 3.6 + pipenv
- PostgreSQL 10 + PostGIS 2.4.4
- Git
- Apache + mod_wsgi
- NodeJs with Microsoft Build Tools (option of NodeJs installer)


## Deploy

### Back-end

1. Clone this repository

```powershell
git clone https://github.com/sitn/perturbtrafic.git
cd perturbtrafic
cd apache
cp app.wsgi.sample app.wsgi
cp wsgi.conf.sample wsgi.conf
cd ..
```

2. In the folder `apache`, edit `app.wsgi` and `wsgi.conf` with the paths where your api is located.

3. Install the api

```powershell
cd back
$env:PIPENV_VENV_IN_PROJECT="true"
pipenv install
pipenv shell
pip install -e .
cp production.ini.sample production.ini
```

4. Configure the api with `production.ini` file.

5. You can test your app by serving it through pserve without errors

```powershell
pserve production.ini
```

If you have errors check troubleshooting section.

6. Kill pserve with <kbd>CTRL</kbd>+<kbd>C</kbd> and go back to the root of your app

```powershell
cd ..
```

7. Check if it runs with Apache

`mod_wsgi` must be installed. Edit your `httpd.conf` file to include the app .conf files like this:

```apache
Include /path/to/your/apache/folder/in/app/*.conf
```

Restart apache and check this url: http://localhost/perturbtrafic/api/types_evenements

It should answer a JSON that looks like this:

```JSON
[
    {
        "id": 1,
        "description": "Autre"
    },
    {
        "id": 2,
        "description": "Chantier"
    }
```

### Front-end

1. Build your front-end with npm

```powershell
cd front
npm install
npm run build
cp .htaccess dist\PerturbTrafic\.htaccess
cd ..
```

If you are unable to run these steps on servers because of Firewall limitations which avoid access
to aws URLs, then build the front on your computer and copy the dist folder.

2. Make sure your Apache has the right path in `DocumentRoot` parameter. It should link to the `dist/PerturbTrafic` folder newly created by the build.

3. Edit `dist/PerturbTrafic/assets/config/config.json` file and set the right url to the api back-end

4. Restart Apache.

### Scripts

1. Install `requests` system wide with pip:

```powershell
pip install requests
```

2. Change your api url inside both files in `/scripts` folder

3. Create a scheduled task that runs both files.

### Troubleshooting

If this error shows up:

```python
configparser.MissingSectionHeaderError: File contains no section headers.
```

It means something is wrong with encoding. Check either `production.ini` or `setup.py` and change it's encoding to `UTF-8` without BOM.

# Main-Project

Repository for developing the main project

## Environment
### Creating an environment
```python
1. python -m venv env # Creates local environment
2. pip install -r requirements.txt # Installs packages included in the file
```
### Activating an environment
Environment needs to be activated before starting the project.

```python
source venv/bin/activate # on Linux/Mac etc.
source venv/Scripts/activate # on Windows
```

### Adding a new package to the Environment
After adding a new package, please make sure you have also updated 'requirements.txt' file with the following command:

```python
pip freeze > requirements.txt
```

## Django

### Starting the Project

```bash
cd BackEnd/
python manage.py runserver 8080
```


### Admin Page

Login details:

username: gdp
password gdp
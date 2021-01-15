# Main-Project

Welcome to the repository for developing the project.
The following steps are to help you set up your IDE environment.
## Environment
### Requirements for the Environment
The package Tensorflow==1.8.0 is required in this project. This package only works up to Python~=3.6.

Note: Installing Tensorflow==1.8.0 automatically updates DoWhy==0.2 --> 0.5. 
After installing Tensorflow, reinstall Dowhy to match the requirements (DoWhy==0.2)
## Environment
### Creating an environment
Conda
```python
1. conda create -n my_env python=3.6 anaconda # Creates local Conda environment. my_env is the name of your environment.
2. pip install -r requirements.txt
```
venv
```python
1. python -m venv env # Creates local environment
2. pip install -r requirements.txt # Installs packages included in the file
```
### Activating an environment
Environment needs to be activated before starting the project.

Conda
```python
conda activate my_env # Activates Conda environment
```
venv
```python
source venv/bin/activate # on Linux/Mac etc.
source venv/Scripts/activate # on Windows
```

### Adding a new package to the Environment
After adding a new package, please make sure you have also updated 'requirements.txt' file with the following command:

```python
pip freeze > requirements.txt
```
Please note that there are many packages required for the system to run. This may take up to an hour to install all necessary packages.

## Django

### Starting the Project

```bash
cd BackEnd/
python manage.py runserver
```


### Admin Page
While running the server admin page can be accessed from:
```bash
http://127.0.0.1:8000/admin
```
Login details:
```bash
username: gdp
password gdp
```

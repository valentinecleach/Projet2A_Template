# Prerequisite:  PDM 


Install PDM for your user with pip 

`> pip install --user pdm`


Check your PDM version with 

`> pdm --version`

## In case of `pdm: command not found`

You must then add the PDM executable to your PATH environment 

To do so: 

Locate the folder in which pdm was installed with `pip list -v` (Usually `C:/Users/UserName/AppData/Roaming or Local/Python/Python310/site-packages`)

Find the `Scripts` folder which is a sibling of the `site-packages` (e.g. `C:/Users/UserName/AppData/Roaming or Local/Python/Python310/Scripts`; it should contain `pdm.exe`) and copy it. 

On Windows, search `Edit the system environment variables`

In `System Properties`, click `Environment variables` => One of the `User variables` should be named `Path`

`Edit` it and add the copied folder at the end of the variable, then save. 

You can now open a new terminal and retry 

# How to install the app 

`> python -m pdm install`

That's all 😊

# Before runing the app 

You must change your file .env with the information of your database

# Connection to Database
dbname="id2464"
user="id2464"
password="id2464"
host="sgbd-eleves.domensai.ecole"
port="5432"

# Schemas names

#schema="projet_info"
#schema="projet_info_test" 
schema="test_projet_info"

# TMDB
TMDB_API_KEY="fb0e5ded3d79bc5e571538030f7e5af8"
TMDB_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjBlNWRlZDNkNzliYzVlNTcxNTM4MDMwZjdlNWFmOCIsIm5iZiI6MTcyNjY2ODg3MS44OTQ2MjMsInN1YiI6IjY2ZTBhYmMyOWM3MzUzMmRkYmFhYWY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cZ0F3epj5FCX4MRlrqSAIdzErJP98tU9ZlfNHkrfUw0"

# JWT_SECRET

JWT_SECRET = ClementValot 
JWT_EXPIRATION_TIME=3600
# How to run the app 


```> pdm start```

This starts a server accessible on `localhost:8000`

The API is then documented on `localhost:8000/docs`

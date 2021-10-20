# Planety task flask-postgresql 
#### Ahmed Masmoudi
#Introduction
This application is base on flask to handle the requests.
The database of choice is postgresql with the initial csv data uploaded there at the first run of the application.
And we are using flask SQLAlchemy and flask migrate to handle the querying the database for specific data entries and to save the updates
and the changes in the local database in a migrations folder.


# Create Postgresql database 'planetly'
```
CREATE DATABASE planetly
```

# Run Postgresql docker in local
```
docker run --name mypostgres -e POSTGRES_PASSWORD=postgres -d postgres
```

Set password is postgres

# Initialize the migration folder 
Initialize the migration folder for the migrate files of your updates later.
```
flask db init
```

# How to add data model
Add Data model to the database, which is define with its schema in a class on app.py
```
flask db migrate 
```
# Deploy database changes
```
flask db upgrade
```
And it will create data table in postgres.

# Initial data upload form csv file

In app.py, the script will check if the data from the csv file is already imported to the database.
The script will only import data from the file if it is not already imported.
This is very important to avoid the overwriting of the changes.
The process is fully automated and does not require additional steps.

# Examples (Question 2)
c. http://127.0.0.1:5000/top?start_dt=1743-11-01&end_dt=1744-10-01&n_city=10

This request will return the top N cities with the highest temperatures in a defined date range of choice.
You only need to define the start date and end date as parameters here and the number of cities to show in the response.


# Examples (Question 3)
a. http://127.0.0.1:5000/highest

This request will return the City with the highest temperature since the year 2000.

b. http://127.0.0.1:5000/add?dt=2020-01-01&AverageTemperature=5.0&AverageTemperatureUncertainty=15.0&City=Schmalkalden&Country=Germany&Latitude=57.05N&Longitude=10.33E

This request will add a new entry with the features as parameters defined with their respective values.

c. http://127.0.0.1:5000/update?dt=2020-01-01&AverageTemperature=2.5&AverageTemperatureUncertainty=15.0&City=Schmalkalden

This request will update the already created new entry by only defining the date of record and the city to update, and the temperature values defined as parameters too.
It will go through the database and look for that specific entry based on date and city and will update the temperatures.
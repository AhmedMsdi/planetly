from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json
from flask import Response
from csv import reader


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@127.0.0.1:5432/planetly"
app.app_context().push()

db = SQLAlchemy()
db.init_app(app)

class Data(db.Model):
    __tablename__ = 'data'
    _id = db.Column('id', db.Integer, primary_key=True)

    dt = db.Column(db.Date(), nullable=True)
    AverageTemperature = db.Column(db.Float(), nullable=True)
    AverageTemperatureUncertainty = db.Column(db.Float(), nullable=True)
    City = db.Column(db.String(), nullable=True)
    Country = db.Column(db.String(), nullable=True)
    Latitude = db.Column(db.String(), nullable=True)
    Longitude = db.Column(db.String(), nullable=True)

    def __init__(self, dt, AverageTemperature, AverageTemperatureUncertainty, City, Country, Latitude, Longitude):
        self.dt = dt
        self.AverageTemperature = AverageTemperature
        self.AverageTemperatureUncertainty = AverageTemperatureUncertainty
        self.City = City
        self.Country = Country
        self.Latitude = Latitude
        self.Longitude = Longitude


if 'data' in db.engine.table_names():
    if Data.query.get(1) is None:

        with open('GlobalLandTemperaturesByCity.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header is not None:
                for row in csv_reader:
                    if str(row[1]) == '':
                        if str(row[2]) == '':
                            exp = Data(row[0], None, None, row[3], row[4], row[5], row[6])
                        else:
                            exp = Data(row[0], None, row[2], row[3], row[4], row[5], row[6])
                    else:
                        exp = Data(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    db.session.add(exp)
                    db.session.commit()

Migrate(app, db)


@app.route('/add', methods=['POST', 'GET'])
def add_new_entry():
    dt = request.args.get('dt')
    AverageTemperature = request.args.get('AverageTemperature')
    AverageTemperatureUncertainty = request.args.get('AverageTemperatureUncertainty')
    City = request.args.get('City')
    Country = request.args.get('Country')
    Latitude = request.args.get('Latitude')
    Longitude = request.args.get('Longitude')
    new_row = Data(dt, AverageTemperature, AverageTemperatureUncertainty, City, Country, Latitude, Longitude)
    db.session.add(new_row)
    db.session.commit()
    return 'New entry created'


@app.route('/update', methods=['POST', 'GET'])
def update_entry():
    dt = request.args.get('dt')
    AverageTemperature = request.args.get('AverageTemperature')
    AverageTemperatureUncertainty = request.args.get('AverageTemperatureUncertainty')
    City = request.args.get('City')

    entry = Data.query.filter(Data.dt == dt).filter(Data.City == City).first()
    entry.AverageTemperature = AverageTemperature
    entry.AverageTemperatureUncertainty = AverageTemperatureUncertainty
    db.session.commit()
    return 'Entry Updated'


@app.route('/top', methods=['POST', 'GET'])
def top_N_cities():
    n_city = request.args.get('n_city')
    start_dt = request.args.get('start_dt')
    end_dt = request.args.get('end_dt')
    result = Data.query.filter(Data.AverageTemperature != None).filter(Data.dt >= start_dt).filter(Data.dt <= end_dt).order_by(
        Data.AverageTemperature.desc()).limit(int(n_city)).all()

    result_cities = []
    for i in range(len(result)):
        result_cities.append(str(result[i].dt) + ',' + str(result[i].AverageTemperature) + ',' + str(result[i].City))
    return 'Top N cities' + str(result_cities)

@app.route('/highest', methods=['POST', 'GET'])
def highest_city():

    result = Data.query.filter(Data.AverageTemperature != None).filter(Data.dt >= '2000-01-01').order_by(
        Data.AverageTemperature.desc()).first()

    return 'Highest rate City since 2000' + str(result.AverageTemperature)




if __name__ == "__main__":
    app.run()

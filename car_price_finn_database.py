#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:28:02 2018

@author: raf
"""
from os import path
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, sessionmaker

import car_price_finn

database_filename = 'finn_cars.sqlite3'

directory = path.abspath(path.dirname(__file__))
database_filepath = path.join(directory, database_filename)

engine_url = 'sqlite:///{}'.format(database_filepath)

engine = create_engine(engine_url)

# Our database class objects are going to inherit from
# this class
Base = declarative_base(bind=engine)

# create a configured “Session” class
Session = sessionmaker(bind=engine, autoflush=False)

# Create a Session
session = Session()

class CarAd(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    price = Column(Integer)
    km = Column(Integer)
    sold = Column(Boolean)
    kode = Column(String, nullable=False, unique=True)
    
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('CarModel', backref='ads')

    def __repr__(self):
        return "CarAd <%r, %r, %r>" % (self.title, self.year, self.director)


class CarModel(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    maker_id = Column(Integer, ForeignKey('makers.id'))
    maker = relationship('CarMaker', backref='models')
    fuel_id = Column(Integer, ForeignKey('fuels.id'))
    fuel = relationship('CarFuel', backref='models')
    body_id = Column(Integer, ForeignKey('bodies.id'))
    body = relationship('CarBody', backref='models')

    def __repr__(self):
        return "CarModel <%r, %r, %r>" % (self.maker, self.name, self.year)


class CarMaker(Base):
    __tablename__ = 'makers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return "CarMaker <%r>" % (self.name)


class CarBody(Base):
    __tablename__ = 'bodies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True, unique=True)

    def __repr__(self):
        return "CarBody <%r>" % (self.name)


class CarFuel(Base):
    __tablename__ = 'fuels'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True, unique=True)
    
    def __repr__(self):
        return "CarFuel <%r>" % (self.name)


def init_db():
    Base.metadata.create_all()


if not path.isfile(database_filepath):
    init_db()


def save_to_database(cars, data):
    
    for car, data_key in zip(cars, data):
        
        # Car Maker
        try:
            maker = session.query(CarMaker).filter_by(name=car.maker).one()
        except NoResultFound:
            maker = CarMaker(name=car.maker)
            session.add(maker)
        
        # Car Fuel
        try:
            fuel = session.query(CarFuel).filter_by(name=car.fuel).one()
        except NoResultFound:
            fuel = CarFuel(name=car.fuel)
            session.add(fuel)
        
        # Car Body
        try:
            body = session.query(CarBody).filter_by(name=car.body).one()
        except NoResultFound:
            body = CarBody(name=car.body)
            session.add(body)
    
        # Car Model
        # need to also fill makers.id, fuels.id, bodies.id
        try:
            model = session.query(CarModel).filter_by(name=car.model, 
                                                      maker_id=maker.id,
                                                      fuel_id=fuel.id, 
                                                      body_id=body.id).one()
        except NoResultFound:
            model = CarModel(name=car.model, maker=maker, fuel=fuel, body=body)
            session.add(model)
            
        # And finally, add advertisement after checking if already in database
        for _, row in data[data_key].iterrows():
            try:
                ad = session.query(CarAd).filter_by(kode=row['kode']).one()
                # Here the ad is already in the database, checking for changes
                if (ad.sold == False) and (row['kr'] == 'Solgt'):
                    ad.sold = True
            except NoResultFound:
                ad = CarAd(model=model,
                           year=row['year'],
                           km=row['km'],
                           price=row['kr'] if not row['kr'] == 'Solgt' else 0,
                           sold=row['kr'] == 'Solgt',
                           kode=row['kode'])
        
                session.add(ad)

        session.commit()
    
    




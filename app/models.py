# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from app import db





class AssetsForecast(db.Model):
    __tablename__ = 'assets_forecast'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.ForeignKey('assets_tables.date', ondelete='CASCADE'), index=True)
    bidopen_forcast = db.Column(db.Float(asdecimal=True))
    bidclose_forcast = db.Column(db.Float(asdecimal=True))
    bidhigh_forcast = db.Column(db.Float(asdecimal=True))
    bidlow_forcast = db.Column(db.Float(asdecimal=True))
    askopen_forcast = db.Column(db.Float(asdecimal=True))
    askclose_forcast = db.Column(db.Float(asdecimal=True))
    askhigh_forcast = db.Column(db.Float(asdecimal=True))
    asklow_forcast = db.Column(db.Float(asdecimal=True))
    tickqty_forcast = db.Column(db.BigInteger)

    assets_table = db.relationship('AssetsTable', primaryjoin='AssetsForecast.date == AssetsTable.date', backref='assets_forecasts')


t_assets_tables = db.Table(
    'assets_tables',
    db.Column('date', db.DateTime, index=True),
    db.Column('bidopen', db.Float(asdecimal=True)),
    db.Column('bidclose', db.Float(asdecimal=True)),
    db.Column('bidhigh', db.Float(asdecimal=True)),
    db.Column('bidlow', db.Float(asdecimal=True)),
    db.Column('askopen', db.Float(asdecimal=True)),
    db.Column('askclose', db.Float(asdecimal=True)),
    db.Column('askhigh', db.Float(asdecimal=True)),
    db.Column('asklow', db.Float(asdecimal=True)),
    db.Column('tickqty', db.BigInteger)
)

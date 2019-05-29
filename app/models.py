# coding: utf-8
from app import db


class StockPrediction(db.Model):
    __tablename__ = 'stock_prediction'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    train_history_id = db.Column(db.Integer, db.ForeignKey('train_history.id'), nullable=False)
    date = db.Column(db.DateTime, index=True)
    bidopen = db.Column(db.Float(asdecimal=True))
    bidclose = db.Column(db.Float(asdecimal=True))
    bidhigh = db.Column(db.Float(asdecimal=True))
    bidlow = db.Column(db.Float(asdecimal=True))
    askopen = db.Column(db.Float(asdecimal=True))
    askclose = db.Column(db.Float(asdecimal=True))
    askhigh = db.Column(db.Float(asdecimal=True))
    asklow = db.Column(db.Float(asdecimal=True))
    tickqty = db.Column(db.BigInteger)

    def add_cotations(self, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty):
        #data[["bidopen","bidclose","bidhigh","bidlow","askopen","askclose","askhigh","asklow","tickqty"]]
        self.bidopen = bidopen[0]
        self.bidclose = bidclose[0]
        self.bidhigh = bidhigh[0]
        self.bidlow = bidlow[0]
        self.askopen = askopen[0]
        self.askclose = askclose[0]
        self.askhigh = askhigh[0]
        self.asklow = asklow[0]
        self.tickqty = tickqty[0]



class StockHistory(db.Model):
    __tablename__ = 'stock_history'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.DateTime, index=True)
    bidopen = db.Column(db.Float(asdecimal=True))
    bidclose = db.Column(db.Float(asdecimal=True))
    bidhigh = db.Column(db.Float(asdecimal=True))
    bidlow = db.Column(db.Float(asdecimal=True))
    askopen = db.Column(db.Float(asdecimal=True))
    askclose = db.Column(db.Float(asdecimal=True))
    askhigh = db.Column(db.Float(asdecimal=True))
    asklow = db.Column(db.Float(asdecimal=True))
    tickqty = db.Column(db.BigInteger)

    def serialize(self):
        return { 'id': self.id,
                 'Date': str(self.date),
                 'bidopen': float(self.bidopen),
                 'bidclose':  float(self.bidclose),
                 'bidhigh': float(self.bidhigh),
                 'bidlow': float(self.bidlow),
                 'askopen': float(self.askopen),
                 'askclose': float(self.askclose),
                 'askhigh': float(self.askhigh),
                 'asklow': float(self.asklow),
                 'tickqty ': self.tickqty
                 }


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stock_predictions = db.relationship('StockPrediction', backref='asset', cascade="all,delete", lazy=True)
    stock_historys = db.relationship('StockHistory', backref='asset', cascade="all,delete", lazy=True)

    def __init__(self, name):
        self.name = name


class TrainHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epochs = db.Column(db.Integer)
    batch_size = db.Column(db.Integer)
    time_steps = db.Column(db.Integer)
    total_train = db.Column(db.Integer)
    total_validation = db.Column(db.Integer) 
    total_test = db.Column(db.Integer)
    score_train = db.Column(db.Float(asdecimal=True))
    score_validation = db.Column(db.Float(asdecimal=True))
    score_test = db.Column(db.Float(asdecimal=True))
    filename = db.Column(db.String(255))
    stock_predictions = db.relationship('StockPrediction', backref='train_history', cascade="all,delete", lazy=True)

    def __init__(self, epochs=epochs, batch_size=batch_size, time_steps=time_steps):
        self.epochs = epochs
        self.batch_size = batch_size
        self.time_steps = time_steps

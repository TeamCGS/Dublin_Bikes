from flask_login import UserMixin
from Dublin_Bikes import db
    
class Static(UserMixin, db.Model):
    """
    Create an Stations table
    """
    __tablename__ = 'Stations'
    
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String (100), nullable=False)
    address = db.Column(db.String (100), nullable=False)
    location_latitude = db.Column(db.Float, nullable=False)
    location_longitude = db.Column(db.Float, nullable=False)
    banking = db.Column(db.Boolean, nullable=False)
    bonus = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, number=None, name=None, address=None, location_latitude=None, location_longitude=None, banking=None, bonus=None):
        self.number = number
        self.name = name
        self.address = address
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self. banking = banking
        self.bonus = bonus
    
    def __repr__(self):
        return '<Static: {}>'.format(self.name)
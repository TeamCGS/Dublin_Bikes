from Dublin_Bikes import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

    
class Static(Base):
    """
    Create an Stations table
    """
    __tablename__ = 'Stations'
    
    address = Column(String (100), nullable=False)
    available_bike_stands = Column(Integer, nullable=False)
    available_bikes = Column(Integer, nullable=False)
    banking = Column(Boolean, nullable=False)
    bike_stands = Column(Integer, nullable=False)
    bonus = Column(Boolean, nullable=False)
    contract_name = Column(String (100), nullable=False)
    last_update = Column(Integer, nullable=False)
    name = Column(String (100), nullable=False)
    number = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    status = Column(String (100), nullable=False)
    
    def __repr__(self):
        return '<Static: {}>'.format(self.name)

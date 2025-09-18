from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///crypto.db')
Session = sessionmaker(bind=engine)
session = Session()


class CryptoCoin(Base):
    __tablename__ = 'cryptocurrency'
    
    id = Column(Integer, primary_key=True)
    name_coin = Column(String)
    symbol = Column(String)
    price = Column(Float)
    trading_volume = Column(Float)
    market_cap = Column(Float)


Base.metadata.create_all(engine)



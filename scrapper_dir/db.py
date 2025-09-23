import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, \
    text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import delete

Base = declarative_base()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "crypto.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)


class CryptoCoin(Base):
    __tablename__ = 'cryptocurrency'
    
    id = Column(Integer, primary_key=True)
    name_coin = Column(String)
    symbol = Column(String)
    price = Column(Float)
    trading_volume = Column(Float)
    market_cap = Column(Float)
    date_added = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )


def add_to_db(data) -> int:
    """Добавляет записи в базу данных"""
    objects = [CryptoCoin(
        name_coin=name_crypto,
        symbol=symbol_crypto,
        price=price,
        trading_volume=trading_volume,
        market_cap=market_cap
    ) for (name_crypto, symbol_crypto, price, trading_volume, market_cap) in
        data]
    
    with Session() as session:
        session.add_all(objects)
        session.commit()
        return len(objects)


def get_all_data():
    """Выдаёт все записи из базы данных"""
    with Session() as session:
        coins = session.query(CryptoCoin).all()
        for coin in coins:
            yield (coin.id, coin.name_coin, coin.symbol, coin.price,
                   coin.trading_volume, coin.market_cap, coin.date_added)


def get_symbol_all(symbol: str) -> list[tuple[datetime, float]]:
    """Выдаёт по символу (например, 'BTC')  -> [(date_added, price)]"""
    with Session() as session:
        rows = (
            session.query(CryptoCoin.date_added, CryptoCoin.price)
            .filter(CryptoCoin.symbol == symbol)
            .order_by(CryptoCoin.date_added.asc()).all())
    return [(r[0], r[1]) for r in rows]


def clean_db():
    """Очищает базу данных"""
    with Session() as session:
        session.execute(delete(CryptoCoin))
        session.commit()
        print("Таблица очищена.")


Base.metadata.create_all(engine)

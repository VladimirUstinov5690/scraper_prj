from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, \
    func, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import delete

Base = declarative_base()
engine = create_engine('sqlite:///crypto.db')
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


def write_to_db(data) -> int:
    """Добавляет записи в БД"""
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
    with Session() as session:
        coins = session.query(CryptoCoin).all()
        for coin in coins:
            yield (coin.id, coin.name_coin, coin.symbol, coin.price,
                   coin.trading_volume, coin.market_cap, coin.date_added)


def clean_db():
    with Session() as session:
        session.execute(delete(CryptoCoin))
        session.commit()
        print("Таблица очищена.")


Base.metadata.create_all(engine)

if __name__ == '__main__':
    clean_db()

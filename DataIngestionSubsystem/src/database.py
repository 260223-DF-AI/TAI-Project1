from datetime import date
import psycopg2
import os
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, create_engine
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.orm import DeclarativeBase, Mapped, Mapped, mapped_column, relationship

# build schema in sql and have python do the rest

# load_dotenv()
# _CS = os.getenv('CS')
# _engine = create_engine(_CS)

# query = f'SELECT * FROM {table_name}'
# df = pd.read_sql(query, engine)

# df.to_sql(name=f"{table_name}", conn=engine, index=False, if_engine='replace', dtype={'colName':'colType'})

# Python on left, sql on right

class Base(DeclarativeBase):
    pass

class Business(Base):
    __tablename__ = 'businesses'

    account_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(500), nullable=False)

    permit: Mapped["Permit"] = relationship(back_populates='business')

class Location(Base):
    __tablename__ = 'locations'

    loc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latitude: Mapped[float] = mapped_column(Numeric(14,11))
    longitude: Mapped[float] = mapped_column(Numeric(14,11))
    site_num: Mapped[int] = mapped_column(Integer, nullable=False)
    address_num: Mapped[str] = mapped_column(String(30), nullable=False)
    street_dir: Mapped[str] = mapped_column(String(1), nullable=True)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    street_type: Mapped[str] = mapped_column(String(30))
    zipcode: Mapped[str] = mapped_column(String(30), nullable=False)

    permit: Mapped["Permit"] = relationship(back_populates='location')

class Permit(Base):
    __tablename__ = 'permits'

    permit_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_num: Mapped[int] = mapped_column(Integer, ForeignKey('businesses.account_num'), nullable=False)
    loc_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.loc_id'))
    opper_name: Mapped[str] = mapped_column(String(500), nullable=False)
    issued_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)

    businesses: Mapped[list["Business"]] = relationship(back_populates='permits')
    sites: Mapped[list["Location"]] = relationship(back_populates="permits")

# Base.metadata.drop_all(_engine)
# Base.metadata.create_all(_engine)

class Database:
    def __init__(self):
        load_dotenv()
        self._CS = os.getenv('CS')
        
        self._engine = create_engine(self._CS)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def insert_into_businesses(self, df: pd.DataFrame):
        df.to_sql(name='businesses', con=self._engine, index=False, if_exists='append')
        #Base.metadata.create_all(self._engine)

    def insert_into_locations(self, df: pd.DataFrame):
        df.to_sql(name='locations', con=self._engine, index=False, if_exists='append')
        #Base.metadata.create_all(self._engine)

    def insert_into_permits(self, df: pd.DataFrame):
        df.to_sql(name='permits', con=self._engine, index=False, if_exists='append')
        #Base.metadata.create_all(self._engine)

    def commit_changes(self):
        Base.metadata.create_all(self._engine)
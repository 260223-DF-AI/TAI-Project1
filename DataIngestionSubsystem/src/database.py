from datetime import date
import os
import psycopg2
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, create_engine
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.orm import DeclarativeBase, Mapped, Mapped, mapped_column, relationship

# build schema in sql and have python do the rest

# load_dotenv()
# CS = os.getenv('CS')
# engine = create_engine(CS, echo=True)

# query = f'SELECT * FROM {table_name}'
# df = pd.read_sql(query, engine)

# df.to_sql(name=f"{table_name}", conn=engine, index=False, if_engine='replace', dtype={'colName':'colType'})

# Python on left, sql on right
class Base(DeclarativeBase):
    pass

class Business(Base):
    __tablename__ = 'businesses'

    account_num: Mapped[int] = mapped_column("ACCOUNT NUMBER", Integer, primary_key=True)
    legal_name: Mapped[str] = mapped_column("LEGAL NAME", String(500), nullable=False)
    opper_name: Mapped[str] = mapped_column("DOING BUSINESS AS NAME", String(500), nullable=False)

    permit: Mapped["Permit"] = relationship(back_populates='business')

class Location(Base):
    __tablename__ = 'locations'

    site_num: Mapped[int] = mapped_column("SITE NUMBER", Integer, primary_key=True)
    lat: Mapped[float] = mapped_column("LATITUDE", Numeric(14,11), nullable=True)
    long: Mapped[float] = mapped_column("LONGITUDE", Numeric(14,11), nullable=True)
    address_num: Mapped[int] = mapped_column("ADDRESS NUMBER", String(30), nullable=False)
    street_dir: Mapped[str] = mapped_column("STREET DIRECTION", String(1), nullable=True)
    street: Mapped[str] = mapped_column("STREET", String(100), nullable=False)
    street_type: Mapped[str] = mapped_column("STREET TYPE", String(30))
    zipcode: Mapped[str] = mapped_column("ZIP CODE", String(30), nullable=False)

    permit: Mapped["Permit"] = relationship(back_populates='location')

class Permit(Base):
    __tablename__ = 'permits'

    permit_num: Mapped[int] = mapped_column("PERMIT NUMBER", Integer, primary_key=True)
    account_num: Mapped[int] = mapped_column("ACCOUNT NUMBER", Integer, ForeignKey('businesses.account_num'), nullable=False)
    site_num: Mapped[int] = mapped_column("SITE NUMBER", Integer, ForeignKey('locations.site_num'), nullable=False)
    issued_date: Mapped[date] = mapped_column("ISSUED DATE", Date, nullable=False)
    expiration_date: Mapped[date] = mapped_column('EXPIRATION DATE', Date, nullable=False)
    payment_date: Mapped[date] = mapped_column("PAYMENT DATE", Date, nullable=False)

    businesses: Mapped[list["Business"]] = relationship(back_populates='permits')
    sites: Mapped[list["Location"]] = relationship(back_populates="permits")

#Base.metadata.create_all(engine)
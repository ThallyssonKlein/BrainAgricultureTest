# src/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String(14), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)

    farms = relationship("Farm", back_populates="farmer")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    arable_area = Column(Float, nullable=False)
    vegetation_area = Column(Float, nullable=False)
    total_area = Column(Float, nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)

    farmer = relationship("Farmer", back_populates="farms")
    crops = relationship("Crop", back_populates="farm")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    culture_id = Column(Integer, ForeignKey("cultures.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="crops")
    culture = relationship("Culture", back_populates="crops")


class Culture(Base):
    __tablename__ = "cultures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    crops = relationship("Crop", back_populates="culture")

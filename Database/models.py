from sqlalchemy import (
    String,
    BigInteger,
    Integer,
    Boolean,
    ForeignKey,
    Enum,
    Float,
    DateTime,
    Date,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Database.database import Base
from datetime import datetime


class PlaceHistory(Base):
    __tablename__ = "place_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    date_time_check:  Mapped[datetime] = mapped_column(DateTime, nullable=False)
    marketplace: Mapped[str] = mapped_column(String, nullable=False)
    vendor_code: Mapped[str] = mapped_column(String, nullable=False)
    place: Mapped[int] = mapped_column(Integer, nullable=False)
    search_text: Mapped[str] = mapped_column(String, nullable=False)
    
class Cards(Base):
    __tablename__ = "cards"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    marketplace: Mapped[str] = mapped_column(String, nullable=False)
    card_name: Mapped[str] = mapped_column(String, nullable=False)
    vendor_code: Mapped[str] = mapped_column(String, nullable=False)
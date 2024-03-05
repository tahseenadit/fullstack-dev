from sqlalchemy import Column, Integer, String
from config import Base


class Sample(Base):
    """Represents a sample table   
    """

    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

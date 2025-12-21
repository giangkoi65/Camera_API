from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    resolution = Column(String(100), default="1920x1080")
    status = Column(String(50), default="active")
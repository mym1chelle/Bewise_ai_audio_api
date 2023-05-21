import uuid
import datetime
from sqlalchemy import Column, UUID, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.db import Base


class Record(Base):
    __tablename__ = 'records'

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    filename = Column(String(100))
    path = Column(String(256))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False
    )
    created_by = relationship('User', back_populates="records")

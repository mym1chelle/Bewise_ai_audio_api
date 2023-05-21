import uuid
from sqlalchemy import Column, UUID, String, LargeBinary
from data.db import Base


class AudioRecording(Base):
    __tablename__ = 'audio_recordings'

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name = Column(String(100))
    data = Column(LargeBinary)
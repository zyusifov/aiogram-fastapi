from sqlalchemy import Boolean, Column, BigInteger, String, DateTime
from datetime import datetime
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)  # Telegram user_id
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)

    referral_code = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
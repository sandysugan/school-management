
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    status = Column(Integer, default=1)  # 1 = active, 0 = used/expired
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by=Column(Integer)
    
    user = relationship("User", back_populates="otps")

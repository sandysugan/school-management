from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from app.core.config import settings



engine = create_engine(
                    settings.DATA_BASE 
                    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


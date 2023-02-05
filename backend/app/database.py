from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# DATABASE_URL = f"postgresql://{os.environ.get ('PGUSER') }:{os.environ.get('PGPASSWORD') }@{os.environ.get('PGHOST') }:{os.environ.get('PGPORT') }/{os.environ.get('PGDATABASE') }"
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
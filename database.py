from sqlmodel import SQLModel, create_engine, Session
from models import ToDo

# Database file name
sqlite_file_name = "database.db"

# Connection URL for SQLite
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create the engine
engine = create_engine(sqlite_url, echo=True)

# Create table(s) from SQLModel classes
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session

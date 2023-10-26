from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Hello


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/ping")
async def ping():
    """
    Endpoint for connection test purposes.
    """
    return {"message": "pong!"}


@app.get("/test_db")
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint for database connection test purposes.
    """
    data = db.query(Hello).first()
    if data:
        return {"message": f"Stored value: {data.name}"}
    else:
        return {"message": "The database is empty."}

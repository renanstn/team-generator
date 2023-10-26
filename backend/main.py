from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
import models, schemas


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/ping")
async def ping():
    """
    Endpoint for connection test purposes.
    """
    return {"message": "pong!"}


@app.get("/test_db", response_model=schemas.HelloSchema)
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint for database connection test purposes.
    """
    data = db.query(models.Hello).first()
    return data if data else {"message": "The database is empty."}

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Hello


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.get("/test_db")
async def test_database_connection(db: Session = Depends(get_db)):
    data = db.query(Hello).first()
    return {"Stored value": data.name} if data else {"The database is empty."}

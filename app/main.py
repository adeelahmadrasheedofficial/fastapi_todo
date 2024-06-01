import time
import psycopg2
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastAPI_blog", user="postgres", password="admin1122")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print("You are connected to: ", record, "\n")
        break
    except Exception as error:
        print("Unable to establish database connection.")
        print(f"Error Detail: {error}")
        time.sleep(5)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"data": "Main Page"}

from .database import engine
from . import models
from .routers import post, user

# from random import randrange
# import time
from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)



# Connection to the database for SQL usage
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='admin', password='admin', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print('connection failed', error)
#         time.sleep(1)



@app.get("/")
def root():
    return {"message": "root"}




        

from app.post import Post
from . import models
from .database import engine, get_db

from random import randrange
import time

from fastapi import FastAPI, status, Response, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connection to the database for SQL usage
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='admin', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print('connection failed', error)
        time.sleep(1)


@app.get("/")
def root():
    return {"message": "root"}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    # Using Raw SQL
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    return {"data": post}


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):

    # Using Raw Sql
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()

    # Using ORM
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post = Body(...), db: Session = Depends(get_db)):

    # Using raw sql
    # cursor.execute("""INSERT INTO post (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.is_published))

    # new_post = cursor.fetchone()

    # conn.commit()

    # Using ORM
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # Using Raw SQl
    # cursor.execute("""UPDATE post SET title = %s, content = %s, is_published = %s, rating = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.is_published, post.rating, str(id)))
    # post = cursor.fetchone()
    # conn.commit()


    # Using ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": post_query.first()}
        


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # Using Raw SQL
    # cursor.execute(
    #     """DELETE FROM post WHERE id = %s RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

        

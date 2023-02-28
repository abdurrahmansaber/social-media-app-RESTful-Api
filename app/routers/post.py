from schema import Post, CreatePost, ResponsePost, UserCreate, UserResponse
import models, utils, oauth2
from database import get_db

from typing import List

from fastapi import APIRouter, status, Response, HTTPException, Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/{id}", response_model=ResponsePost)
def get_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    # Using Raw SQL
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

    return post


@router.get("/", response_model=List[ResponsePost])
def get_all_posts(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    # Using Raw Sql
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()

    # Using ORM
    posts = db.query(models.Post).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_post(post: CreatePost , db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    # Using raw sql
    # cursor.execute("""INSERT INTO post (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.is_published))

    # new_post = cursor.fetchone()

    # conn.commit()

    # Using ORM
    new_post = models.Post(owner_id = user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=ResponsePost)
def update_post(id: int, post: Post, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # Using Raw SQl
    # cursor.execute("""UPDATE post SET title = %s, content = %s, is_published = %s, rating = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.is_published, post.rating, str(id)))
    # post = cursor.fetchone()
    # conn.commit()


    # Using ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_obj = post_query.first()
    if not post_query.first():  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    if post_obj.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO Update OTHERS")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
        


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # Using Raw SQL
    # cursor.execute(
    #     """DELETE FROM post WHERE id = %s RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # Using ORM
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO DELETE OTHERS")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


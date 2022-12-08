from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Body
from post import Post
from random import randrange

app = FastAPI()

posts_dict = {}


@app.get("/")
def root():
    return {"message": "root"}


@app.get("/posts/{id}")
def get_post(id: int):
    if posts_dict.get(id):
        return posts_dict.get(id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    


@app.get("/posts")
def get_all_posts():
    return posts_dict


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post = Body(...)):
    id = randrange(0, 1000000000)
    payload = {id: payload.dict()}
    posts_dict[id] = payload
    print(payload)
    return payload


@app.put("/posts/{id}")
def update_post():
    return None


@app.delete("/posts/{id}")
def delete_post(id: int):
    
    if posts_dict.get(id):
        posts_dict.pop(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

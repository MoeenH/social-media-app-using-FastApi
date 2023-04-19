from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None
    
    

my_posts = [{ "title" : "title of post 1", "content" : "content of the post", "id" : 1 } ]


@app.get("/")
def root():         # main page
    
    return {"message": "Welcome to Api"}

@app.get("/posts")      # to get all posts
def get_post():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post:Post):  # to create posts
    posts_dict = new_post.dict()
    posts_dict["id"] =  randrange(0,1000000)
    my_posts.append(posts_dict)  
    return{"data": posts_dict}



@app.get("/posts/{id}")
def get_post(id: int, response : Response):              # to get a specific post
    if post := find_post(id):
        return{"post_detail" : f"Here is the post {post}"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id : {id} not found")

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id :int,post : Post):
    index = find_index_post(id)
    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post id {id} does not exist")
    post_dict= post.dict()
    my_posts[index] = post_dict
    return {"Message" : "Updated Successfully"}



# ALL FUNCTIONS
def find_post(id):          #to find a specific post
    for i in my_posts:
        if i['id'] == id:
            return i

def find_index_post(id):
        for i, p in enumerate(my_posts):
            if p['id'] == id:
                return i
        
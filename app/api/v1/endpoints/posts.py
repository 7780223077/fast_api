from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies.database import get_db
from typing import List
from app import schemas
from app.models.post import Post
from app.models.user import User
from app.models.vote import Vote
from app.utils import jwtservice

router = APIRouter()

#FOR POSTS
@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostBase, session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    new_post = Post(user_id= current_user.id ,**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.put("/post/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id: int, update_post: schemas.PostBase, session:Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    post_query = session.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id '{id}' does not exist")
   
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to perform actions on this post")
   
    post_query.update(update_post.model_dump(), synchronize_session=False)
    session.commit()

    return  post_query.first()


# @router.get("/posts",response_model= List[schemas.Post])
@router.get("/posts",response_model= List[schemas.PostWithVotes])
async def get_posts(session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user),
                    page:int = 1, size:int = 5):
    # posts = session.query(Post).limit(size).offset((page-1)*size).all() #limit(page-1).offset(size)
    posts = (
        session.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .limit(size)
        .offset((page - 1) * size)
        .all()
    )

    # Convert the result to a list of dictionaries (serializable format)
    # posts = []
    # for post, vote_count in posts_query:
    #     post_data = {
    #         "id": post.id,
    #         "title": post.title,
    #         "content": post.content,
    #         "published": post.published,
    #         "created_at": post.created_at,
    #         "user_id": post.user_id,
    #         "vote_count": vote_count
    #     }
    #     posts.append(post_data)

    return posts


@router.get("/post/{id}", response_model=schemas.Post)
async def get_post(id: int, session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    post = session.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= f"post with id '{id}' was not found"
            )
    return post


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    post_query = session.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id '{id}' was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to perform actions on this post")

    post_query.delete(synchronize_session=False)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
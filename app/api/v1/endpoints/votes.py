
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.vote import Vote
from app.models.user import User
from app.models.post import Post
from app.utils import jwtservice
from app import schemas
router = APIRouter()

# @router.get("/votes")
# async def get_votes(session: Session= Depends(get_db)):
#     votes = session.query(Vote).all()
#     return votes

@router.post("/vote")
async def create_vote(vote: schemas.VoteBase, session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    
    post = session.query(Post).filter(Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = session.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = Vote(user_id = current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        session.commit()
        return {"message": "successfully deleted vote"}


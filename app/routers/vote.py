from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db
from ..schemas import Vote

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    if vote.direction not in [True, False]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Direction must be True (upvote) or False (downvote)")
    
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {vote.post_id} was not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first() # type: ignore
    
    if vote.direction:
        # Check if the user has already voted on this post
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
        
        # Create a new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message": "Post liked successfully"}
    else:
        # If the user is trying to remove a like, check if the vote exists
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not liked this post")
        
        # Delete the vote
        db.delete(vote_query)
        db.commit()
        return {"message": "Post unliked successfully"}
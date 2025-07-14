from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db
from ..schemas import Vote

router = APIRouter(
    prefix="/posts/{id}/vote",
    tags=["Vote"]
)

print("Vote router loaded")

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(id: int, vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    if vote.direction not in [True, False]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Direction must be True (upvote) or False (downvote)")
    
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == id, models.Vote.user_id == current_user.id).first() # type: ignore
    
    if vote.direction:
        # Check if the user has already voted on this post
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
        
        # Create a new vote

        # Check if the user is the owner of the post
        if post.owner_id == current_user.id:  # type: ignore
            # If the user is the owner, set like_by_owner to True
            new_vote = models.Vote(post_id=id, user_id=current_user.id, like_by_owner=True) # type: ignore
        else:
            # If the user is not the owner, set like_by_owner to False
            new_vote = models.Vote(post_id=id, user_id=current_user.id, like_by_owner=False) # type: ignore
        
        post.likes += 1 # type: ignore

        db.add(new_vote)
        db.commit()
        return {"message": "Post liked successfully"}
    else:
        # If the user is trying to remove a like, check if the vote exists
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not liked this post")
        
        post.likes -= 1 # type: ignore

        # Delete the vote
        db.delete(vote_query)
        db.commit()
        return {"message": "Post unliked successfully"}
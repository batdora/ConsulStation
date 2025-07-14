from hmac import new
from .. import models, schemas, oath2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import func, or_
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

print("Post router loaded")

# In this example we require authorization for all post operations.
# If you want to allow unauthenticated access to some endpoints, you can remove the Depends
# from oath2.get_current_user() dependency from those endpoints.

# GET all posts
@router.get("/", response_model=List[schemas.PostSummaryResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "", user_id: Optional[int] = None):
    q = (
        db.query(models.Post)
          .options(selectinload(models.Post.owner))
          .filter(models.Post.reply_to.is_(None))
    )

    if user_id is not None:
        q = q.filter(models.Post.owner_id == user_id)

    if search:
        term = f"%{search}%"
        q = q.filter(
            or_(
                models.Post.title.ilike(term),
                models.Post.content.ilike(term),
            )
        )

    posts = (
        q.order_by(models.Post.created_at.desc())
         .offset(skip)
         .limit(limit)
         .all()
    )

    return posts

# GET ID specific post
@router.get("/{id}",response_model=schemas.PostDetailResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post = (
        db.query(models.Post)
          .options(
              selectinload(models.Post.owner),
              # load each reply and its owner
              selectinload(models.Post.replies)
                  .selectinload(models.Post.owner),
          )
          .filter(models.Post.id == id)
          .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post




# POST a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    new_post = models.Post(**post.model_dump())
    
    # Set the owner_id to the current user's id
    new_post.owner_id = current_user.id # type: ignore
    new_post.original_post_owner_id = current_user.id # type: ignore

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# POST a reply to a post
@router.post("/{id}/reply", status_code=status.HTTP_201_CREATED, response_model=schemas.PostDetailResponse)
def create_reply(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    original_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # Check if the original post exists
    if not original_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The original post or reply with the id: {id} was not found")
    
    # Create a new post as a reply
    new_reply = models.Post(**post.model_dump())
    new_reply.owner_id = current_user.id # type: ignore
    new_reply.reply_to = id  # type: ignore # Set the reply_to to the original post's id
    new_reply.original_post_owner_id = original_post.owner_id  # Set the original post's owner id

    db.add(new_reply)

    original_post.direct_reply_count += 1  # type: ignore # Increment the direct reply count of the original post
    
    ancestor = original_post
    while ancestor.parent:  # type: ignore # Traverse up to the root post
        ancestor.total_reply_count += 1  # type: ignore # Increment the total reply count
        ancestor = ancestor.parent  # type: ignore # Move to the parent post

    db.commit()
    db.refresh(new_reply)
    return new_reply

# DELETE Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    
    # Check if the current user is the owner of the post
    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    # Delete the post
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update with PUT
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    # Check if the post exists
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} was not found")
    
    # Check if the current user is the owner of the post
    if updated_post.first().owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
    
    updated_post.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    return updated_post.first()
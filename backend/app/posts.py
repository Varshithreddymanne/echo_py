from fastapi import APIRouter, HTTPException, Depends, Header
from .database import db
from .models import PostCreate, CommentCreate
from .utils import verify_token
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])

# helper to convert ObjectId -> string
def to_json(doc):
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
async def list_posts():
    cursor = db.posts.find().sort("created_at", -1)
    posts = []
    async for p in cursor:
        posts.append(to_json(p))
    return posts

@router.post("/")
async def create_post(post: PostCreate):
    data = post.dict()
    data.update({"likes": 0, "comments": [], "created_at": datetime.utcnow()})
    result = await db.posts.insert_one(data)
    return {"post_id": str(result.inserted_id)}

@router.post("/{post_id}/like")
async def like_post(post_id: str):
    try:
        oid = ObjectId(post_id)
    except:
        raise HTTPException(400, "Invalid post id")
    res = await db.posts.update_one({"_id": oid}, {"$inc": {"likes": 1}})
    if res.matched_count == 0:
        raise HTTPException(404, "Post not found")
    updated = await db.posts.find_one({"_id": oid})
    return {"likes": updated.get("likes", 0)}

@router.post("/{post_id}/comment")
async def add_comment(post_id: str, comment: CommentCreate):
    try:
        oid = ObjectId(post_id)
    except:
        raise HTTPException(400, "Invalid post id")
    # ensure post exists
    post = await db.posts.find_one({"_id": oid})
    if not post:
        raise HTTPException(404, "Post not found")
    comment_doc = comment.dict()
    comment_doc.update({"post_id": post_id, "created_at": datetime.utcnow()})
    result = await db.comments.insert_one(comment_doc)
    await db.posts.update_one({"_id": oid}, {"$push": {"comments": str(result.inserted_id)}})
    return {"comment_id": str(result.inserted_id)}

@router.get("/{post_id}/comments")
async def get_comments(post_id: str):
    comments = []
    cursor = db.comments.find({"post_id": post_id}).sort("created_at", -1)
    async for c in cursor:
        c = dict(c)
        c["_id"] = str(c["_id"])
        comments.append(c)
    return comments
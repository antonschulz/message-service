from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from . import models, schemas, database

router = APIRouter()


def get_db():
    """
    Yields a SQLAlchemy Session, then closes it when the request is done.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Submit a message to a defined recipient
@router.post(
    "/messages/{recipient_id}",
    response_model=schemas.MessageRead,
    status_code=201,
    summary="Submit a new plain-text message",
)
def create_message_plaintext(
    recipient_id: str,
    body: str = Body(..., media_type="text/plain"),
    db: Session = Depends(get_db),
):
    """
    Create a new plain-text message for {recipient_id}.
    - Path parameter: recipient_id (string)
    - Request body: raw text/plain
    """
    new_msg = models.Message(
        id=None,
        recipient_id=recipient_id,
        body=body,
        created_at=datetime.now(),
        is_read=False,
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg


# Fetch unread messages
@router.get(
    "/messages/unread",
    response_model=List[schemas.MessageRead],
    summary="Fetch all unread messages for a recipient and mark them read",
)
def get_unread_messages(
    recipient_id: str = Query(..., description="The recipient identifier"),
    db: Session = Depends(get_db),
):
    """
    Fetches all messages where is_read == False for this recipient,
    marks each one as read, commits, and returns them.
    """
    unread_msgs = (
        db.query(models.Message)
        .filter(
            models.Message.recipient_id == recipient_id, models.Message.is_read == False
        )
        .order_by(models.Message.created_at.asc())
        .all()
    )

    if not unread_msgs:
        return []

    for msg in unread_msgs:
        msg.is_read = True

    db.commit()

    return unread_msgs


# Delete a single message
@router.delete(
    "/messages/{message_id}",
    status_code=204,
    summary="Delete a single message by ID",
)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete one message by its ID. Returns 204 if deleted, 404 if not found.
    """
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return None


# Delete multiple messages
@router.delete(
    "/messages/",
    response_model=dict,
    summary="Delete multiple messages in one request",
)
def delete_multiple_messages(
    payload: schemas.MessageDeleteMultiple,
    db: Session = Depends(get_db),
):
    """
    Delete multiple messages whose IDs are in payload.message_ids.
    Returns {"deleted_count": <n>}.
    """
    if not payload.message_ids:
        raise HTTPException(
            status_code=400, detail="message_ids list must not be empty"
        )
    q = db.query(models.Message).filter(models.Message.id.in_(payload.message_ids))
    deleted_count = q.delete(synchronize_session=False)
    db.commit()
    return {"deleted_count": deleted_count}


# Fetch messages (including previously fetched) ordered by time, according to stop and/or stop index
@router.get(
    "/messages/",
    response_model=List[schemas.MessageRead],
    summary="Fetch all messages (read or unread) with pagination",
)
def get_messages(
    recipient_id: str = Query(..., description="The recipient identifier"),
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(10, ge=1, description="Max number of messages to return"),
    db: Session = Depends(get_db),
):
    """
    Fetch messages (all, regardless of is_read) for this recipient,
    ordered by created_at descending, using offset/limit for pagination.
    """
    msgs = (
        db.query(models.Message)
        .filter(models.Message.recipient_id == recipient_id)
        .order_by(models.Message.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not msgs:
        return []

    for msg in msgs:
        msg.is_read = True

    db.commit()

    for msg in msgs:
        db.refresh(msg)

    return msgs

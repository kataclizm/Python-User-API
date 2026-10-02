from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_users(db: Session = Depends(get_db)):

    return (
        db.query(User)
        .filter(User.is_deleted == False)
        .all()
    )


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted == False
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.post("/")
def create_user(
        request: UserCreate,
        db: Session = Depends(get_db)
):

    user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{user_id}")
def update_user(
        user_id: int,
        request: UserUpdate,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_deleted = True

    db.commit()

    return {
        "message": "User soft deleted"
    }
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/assign-role")
def assign_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    user.role = role

    db.commit()

    return {"message": "Role assigned successfully"}
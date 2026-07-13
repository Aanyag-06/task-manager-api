from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.helpers import get_team_or_404, get_user_role_in_team
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.activity import ActivityLog

router = APIRouter(prefix="/teams/{team_id}/activity", tags=["Activity"])

@router.get("/")
def get_activity(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    logs = session.exec(
        select(ActivityLog)
        .where(ActivityLog.team_id == team_id)
        .order_by(ActivityLog.created_at.desc())
    ).all()
    return logs
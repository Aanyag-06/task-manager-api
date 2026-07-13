from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.membership import TeamMembership, Role
from app.models.team import Team
from app.models.activity import ActivityLog

def log_activity(action: str, user_id: int, team_id: int, session: Session):
    log = ActivityLog(
        action=action,
        user_id=user_id,
        team_id=team_id
    )
    session.add(log)
    session.commit()

def get_user_role_in_team(user_id: int, team_id: int, session: Session) -> Role:
    """
    Returns the role of a user in a team.
    Raises 403 if the user is not a member of the team.
    """
    membership = session.exec(
        select(TeamMembership).where(
            TeamMembership.user_id == user_id,
            TeamMembership.team_id == team_id
        )
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team"
        )

    return membership.role

def get_team_or_404(team_id: int, session: Session) -> Team:
    """
    Returns a team or raises 404 if it doesn't exist.
    """
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return team
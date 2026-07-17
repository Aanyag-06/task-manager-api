from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.helpers import get_user_role_in_team, get_team_or_404
from app.auth.dependencies import get_current_user
from app.auth.permissions import check_permission
from app.models.user import User
from app.models.team import Team
from app.models.membership import TeamMembership, Role
from app.schemas.team import TeamCreate, InviteMember, ChangeRole, TeamResponse, MemberResponse

router = APIRouter(prefix="/teams", tags=["Teams"])


# Create team
@router.post("/", response_model=TeamResponse, status_code=201)
def create_team(
    team_data: TeamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # create the team
    new_team = Team(
        name=team_data.name,
        description=team_data.description,
        owner_id=current_user.id
    )
    session.add(new_team)
    session.commit()
    session.refresh(new_team)

    # automatically make the creator an Owner
    membership = TeamMembership(
        user_id=current_user.id,
        team_id=new_team.id,
        role=Role.owner
    )
    session.add(membership)
    session.commit()

    return new_team


# Get my team
@router.get("/", response_model=list[TeamResponse])
def get_my_teams(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # find all teams this user is a member of
    memberships = session.exec(
        select(TeamMembership).where(TeamMembership.user_id == current_user.id)
    ).all()

    teams = []
    for m in memberships:
        team = session.get(Team, m.team_id)
        if team:
            teams.append(team)
    return teams


# Get one team
@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    team = get_team_or_404(team_id, session)
    # verify the user is actually in this team
    get_user_role_in_team(current_user.id, team_id, session)
    return team


# Get team members
@router.get("/{team_id}/members", response_model=list[MemberResponse])
def get_members(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    memberships = session.exec(
        select(TeamMembership).where(TeamMembership.team_id == team_id)
    ).all()

    result = []
    for m in memberships:
        user = session.get(User, m.user_id)
        if user:
            result.append(MemberResponse(
                user_id=user.id,
                email=user.email,
                role=m.role
            ))
    return result


# Invite members
@router.post("/{team_id}/invite")
def invite_member(
    team_id: int,
    invite_data: InviteMember,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)

    # check the current user has permission to invite
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "invite_member")

    # find the user being invited by email
    invited_user = session.exec(
        select(User).where(User.email == invite_data.email)
    ).first()
    if not invited_user:
        raise HTTPException(status_code=404, detail="User not found")

    # check they're not already in the team
    existing = session.exec(
        select(TeamMembership).where(
            TeamMembership.user_id == invited_user.id,
            TeamMembership.team_id == team_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a member")

    membership = TeamMembership(
        user_id=invited_user.id,
        team_id=team_id,
        role=invite_data.role
    )
    session.add(membership)
    session.commit()

    return {"message": f"{invited_user.email} added to team with role {invite_data.role}"}


# Change Role
@router.patch("/{team_id}/role")
def change_member_role(
    team_id: int,
    role_data: ChangeRole,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)

    # only owners can change roles
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "change_role")

    # find the target user
    target_user = session.exec(
        select(User).where(User.email == role_data.email)
    ).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    membership = session.exec(
        select(TeamMembership).where(
            TeamMembership.user_id == target_user.id,
            TeamMembership.team_id == team_id
        )
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="User is not in this team")

    membership.role = role_data.role
    session.add(membership)
    session.commit()

    return {"message": f"Role updated to {role_data.role} for {target_user.email}"}


# Remove Member
@router.delete("/{team_id}/members/{user_id}")
def remove_member(
    team_id: int,
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)

    # only owners can remove members
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "remove_member")

    membership = session.exec(
        select(TeamMembership).where(
            TeamMembership.user_id == user_id,
            TeamMembership.team_id == team_id
        )
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="User is not in this team")

    session.delete(membership)
    session.commit()

    return {"message": "Member removed successfully"}
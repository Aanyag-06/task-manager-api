from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.helpers import get_user_role_in_team, get_team_or_404, log_activity
from app.auth.dependencies import get_current_user
from app.auth.permissions import check_permission
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/teams/{team_id}/projects", tags=["Projects"])


# ─── CREATE PROJECT ────────────────────────────────────────────
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    team_id: int,
    data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "create_project")

    project = Project(name=data.name, description=data.description, team_id=team_id)
    session.add(project)
    session.commit()
    session.refresh(project)

    log_activity(f"User {current_user.id} created project '{project.name}'", current_user.id, team_id, session)
    return project


# ─── GET ALL PROJECTS IN A TEAM ────────────────────────────────
@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    projects = session.exec(select(Project).where(Project.team_id == team_id)).all()
    return projects


# ─── GET ONE PROJECT ───────────────────────────────────────────
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    team_id: int,
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    project = session.get(Project, project_id)
    if not project or project.team_id != team_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ─── UPDATE PROJECT ────────────────────────────────────────────
@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    team_id: int,
    project_id: int,
    data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "edit_project")

    project = session.get(Project, project_id)
    if not project or project.team_id != team_id:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = data.name
    project.description = data.description
    session.add(project)
    session.commit()
    session.refresh(project)

    log_activity(f"User {current_user.id} updated project '{project.name}'", current_user.id, team_id, session)
    return project


# ─── DELETE PROJECT ────────────────────────────────────────────
@router.delete("/{project_id}")
def delete_project(
    team_id: int,
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_team_or_404(team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "delete_project")

    project = session.get(Project, project_id)
    if not project or project.team_id != team_id:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()

    log_activity(f"User {current_user.id} deleted project '{project.name}'", current_user.id, team_id, session)
    return {"message": "Project deleted"}
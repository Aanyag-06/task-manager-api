from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.helpers import get_user_role_in_team, log_activity
from app.auth.dependencies import get_current_user
from app.auth.permissions import check_permission
from fastapi import Query   
from app.models.user import User
from app.models.project import Project
from app.models.task import Task, TaskAssignment
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/teams/{team_id}/projects/{project_id}/tasks", tags=["Tasks"])


def get_project_or_404(project_id: int, team_id: int, session: Session) -> Project:
    project = session.get(Project, project_id)
    if not project or project.team_id != team_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# Create task
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    team_id: int,
    project_id: int,
    data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_project_or_404(project_id, team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "create_task")

    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        project_id=project_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # handle assignees
    for user_id in data.assignee_ids:
        assignment = TaskAssignment(task_id=task.id, user_id=user_id)
        session.add(assignment)
    session.commit()

    log_activity(f"User {current_user.id} created task '{task.title}'", current_user.id, team_id, session)
    return task


# Get All Tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    team_id: int,
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    # filtering params — all optional
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    search: str | None = Query(default=None),
    # pagination params
    limit: int = Query(default=10, le=100),   # max 100 per page
    offset: int = Query(default=0)             # how many to skip
):
    get_project_or_404(project_id, team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    query = select(Task).where(Task.project_id == project_id)

    # apply filters only if they were provided
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))  # case-insensitive search

    # apply pagination
    query = query.offset(offset).limit(limit)

    tasks = session.exec(query).all()
    return tasks


# Get one task
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    team_id: int,
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_project_or_404(project_id, team_id, session)
    get_user_role_in_team(current_user.id, team_id, session)

    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update task
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    team_id: int,
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_project_or_404(project_id, team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "edit_task")

    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # only update fields that were actually sent
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status
    if data.priority is not None:
        task.priority = data.priority

    # update assignees if provided
    if data.assignee_ids is not None:
        # delete old assignments first
        old = session.exec(select(TaskAssignment).where(TaskAssignment.task_id == task_id)).all()
        for a in old:
            session.delete(a)
        # add new ones
        for user_id in data.assignee_ids:
            session.add(TaskAssignment(task_id=task_id, user_id=user_id))

    session.add(task)
    session.commit()
    session.refresh(task)

    log_activity(f"User {current_user.id} updated task '{task.title}'", current_user.id, team_id, session)
    return task


# Delete task
@router.delete("/{task_id}")
def delete_task(
    team_id: int,
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_project_or_404(project_id, team_id, session)
    role = get_user_role_in_team(current_user.id, team_id, session)
    check_permission(role, "delete_task")

    task = session.get(Task, task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    log_activity(f"User {current_user.id} deleted task '{task.title}'", current_user.id, team_id, session)
    return {"message": "Task deleted"}
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.helpers import get_user_role_in_team, log_activity
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.project import Project
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(
    prefix="/teams/{team_id}/projects/{project_id}/tasks/{task_id}/comments",
    tags=["Comments"]
)


# ─── ADD COMMENT ───────────────────────────────────────────────
@router.post("/", response_model=CommentResponse, status_code=201)
def add_comment(
    team_id: int,
    project_id: int,
    task_id: int,
    data: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # all roles including viewer can comment
    get_user_role_in_team(current_user.id, team_id, session)

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comment = Comment(content=data.content, task_id=task_id, user_id=current_user.id)
    session.add(comment)
    session.commit()
    session.refresh(comment)

    log_activity(f"User {current_user.id} commented on task {task_id}", current_user.id, team_id, session)
    return comment


# ─── GET COMMENTS ON A TASK ────────────────────────────────────
@router.get("/", response_model=list[CommentResponse])
def get_comments(
    team_id: int,
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    get_user_role_in_team(current_user.id, team_id, session)

    comments = session.exec(select(Comment).where(Comment.task_id == task_id)).all()
    return comments
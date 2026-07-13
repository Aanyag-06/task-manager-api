from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.models.user import User
from app.models.team import Team
from app.models.membership import TeamMembership
from app.models.project import Project
from app.models.task import Task, TaskAssignment
from app.models.comment import Comment
from app.models.activity import ActivityLog
from app.routes.auth import router as auth_router
from app.routes.teams import router as teams_router
from app.routes.projects import router as projects_router
from app.routes.tasks import router as tasks_router
from app.routes.comments import router as comments_router
from app.routes.activity import router as activity_router
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="Task Manager API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Task Manager API"}

@app.get("/health")
def health():
    return {"status": "ok"}
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )

# handles all other HTTP errors (404, 403, 401 etc.)
from fastapi import HTTPException as FastAPIHTTPException

@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "errors": []
        }
    )

app.include_router(auth_router)
app.include_router(teams_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(activity_router)
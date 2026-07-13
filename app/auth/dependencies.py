from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User
from app.auth.jwt_handler import decode_access_token

# tells FastAPI: "look for a Bearer token at /auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # get user id from token payload
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # look up the actual user in the database
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    return user  # this is the logged-in user object
from app.models.membership import Role
from fastapi import HTTPException, status

# This dictionary defines what each role is allowed to do
# True = allowed, False = not allowed
ROLE_PERMISSIONS = {
    "create_project":   {Role.owner: True,  Role.maintainer: True,  Role.member: False, Role.viewer: False},
    "edit_project":     {Role.owner: True,  Role.maintainer: True,  Role.member: False, Role.viewer: False},
    "delete_project":   {Role.owner: True,  Role.maintainer: False, Role.member: False, Role.viewer: False},
    "create_task":      {Role.owner: True,  Role.maintainer: True,  Role.member: True,  Role.viewer: False},
    "edit_task":        {Role.owner: True,  Role.maintainer: True,  Role.member: True,  Role.viewer: False},
    "delete_task":      {Role.owner: True,  Role.maintainer: True,  Role.member: False, Role.viewer: False},
    "invite_member":    {Role.owner: True,  Role.maintainer: True,  Role.member: False, Role.viewer: False},
    "change_role":      {Role.owner: True,  Role.maintainer: False, Role.member: False, Role.viewer: False},
    "remove_member":    {Role.owner: True,  Role.maintainer: False, Role.member: False, Role.viewer: False},
    "add_comment":      {Role.owner: True,  Role.maintainer: True,  Role.member: True,  Role.viewer: True},
    "view":             {Role.owner: True,  Role.maintainer: True,  Role.member: True,  Role.viewer: True},
}

def check_permission(role: Role, action: str):
    """
    Call this function before any sensitive action.
    It automatically raises a 403 error if the role isn't allowed.
    """
    if not ROLE_PERMISSIONS.get(action, {}).get(role, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your role '{role}' is not allowed to perform '{action}'"
        )
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*allowed_roles):
    """
    Usage:
        @role_required("manager")
        @role_required("employee", "manager")
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # verify JWT exists & valid
            verify_jwt_in_request()

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return {
                    "message": "Permission denied",
                    "required_roles": allowed_roles
                }, 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator

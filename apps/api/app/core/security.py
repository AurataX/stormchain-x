from secrets import compare_digest

from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)


def require_operator(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Security(bearer),
):
    expected = request.app.state.settings.operator_token
    if not expected:
        raise HTTPException(503, "Observation writes disabled: operator token not configured")
    if credentials is None or not compare_digest(
        credentials.credentials.encode(), expected.encode()
    ):
        raise HTTPException(
            401, "Invalid operator credentials", headers={"WWW-Authenticate": "Bearer"}
        )

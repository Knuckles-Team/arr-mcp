from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from arr_mcp.utils import get_logger

logger = get_logger(__name__)


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Error processing request: {exc}", exc_info=True)
            raise


class UserTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config=None):
        super().__init__(app)
        self.config = config

    async def dispatch(self, request: Request, call_next):
        # TODO: Implement token validation if needed
        return await call_next(request)


class JWTClaimsLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Implement JWT claims logging if needed
        return await call_next(request)

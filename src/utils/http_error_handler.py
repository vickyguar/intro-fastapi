from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

class HTTPErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    # Lo que hace es simplemente pasar al siguiente middleware o endpoint
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse: # dependiendo si hay error o no
        try:
            return await call_next(request)
        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(content={"message": "Ocurrió un error en el servidor", "details": str(e)}, status_code=status_code)
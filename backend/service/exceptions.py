from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request


class UserError(Exception):
    code: str

    def __init__(self, *args: object, code="bad_request") -> None:
        super().__init__(*args)
        self.code = code


class ServerError(Exception):
    pass


def bind_exceptions(api: FastAPI):
    @api.exception_handler(UserError)
    async def user_error_handler(request: Request, exc: UserError):
        return JSONResponse(
            status_code=400,
            content={"error": {"code": exc.code, "message": f"{exc}"}},
        )

    @api.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "api_error", "message": f"{exc}"}},
        )

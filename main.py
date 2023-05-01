import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from data.models import create_table
from request import urls as request_urls
from users import urls as user_urls
from util.database import create_app


app, api = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_message = f"Unexpected error occurred: {exc}"
    return JSONResponse(status_code=500, content={"detail": error_message})


api.include_router(request_urls.router)
api.include_router(user_urls.router)


app.include_router(api)


if __name__ == "__main__":
    create_table()
    uvicorn.run(app, host="0.0.0.0", port=8000)
